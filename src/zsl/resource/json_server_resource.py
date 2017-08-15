"""
:mod:`zsl.resource.json_server_resource`
----------------------------------------
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
import logging
import re
from typing import Any

from flask import request
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from zsl.interface.resource import ResourceResult
from zsl.resource.resource_helper import filter_from_url_arg, flat_model, model_tree
from zsl.service.service import transactional
from zsl.utils.http import get_http_status_code_value

from .model_resource import ModelResource

NOT_FOUND = ResourceResult(
    body={},
    status=get_http_status_code_value(http.client.NOT_FOUND)
)

NOT_IMPLEMENTED = ResourceResult(
    body={},
    status=get_http_status_code_value(http.client.NOT_IMPLEMENTED)
)

# any other arguments from these are considered as `property_name(_operator)=some_vaule` filter
_SKIPPED_ARGUMENTS = set(['callback', '_', 'q', '_start', '_end', '_sort', '_order', '_limit', '_embed', '_expand'])

# first group is the column name, then it can have a . separator or an operator suffix
_re_column_name = re.compile(r'^([^.]*?)(\..*?)?(_lte|_gte|_ne|_like)?$')


def _page_arg(p):
    # type: (int) -> str
    """Create a page argument from int."""
    return 'page=' + str(p)


def _get_link_pages(page, per_page, count, page_url):
    # type: (int, int, int, str) -> Dict[str, str]
    """Create link header for page metadata.

    :param page: current page
    :param per_page: page limit
    :param count: count of all resources
    :param page_url: url for resources
    :return: dictionary with name of the link as key and its url as value
    """
    current_page = _page_arg(page)
    links = {}
    end = page * per_page

    if page > 1:
        links['prev'] = page_url.replace(current_page, _page_arg(page - 1))

    if end < count:
        links['next'] = page_url.replace(current_page, _page_arg(page + 1))

    if per_page < count:
        links['first'] = page_url.replace(current_page, _page_arg(1))
        links['last'] = page_url.replace(current_page, _page_arg((count + per_page - 1) // per_page))

    return links


class JsonServerResource(ModelResource):
    """Model resource implementation to correspond with json-server.

    This implements the same REST interface which json-server
    (https://github.com/typicode/json-server) uses. It transforms the given
    input arguments into ModelResource-like and then adds metadata to result.
    """
    def to_filter(self, query, arg):
        """Json-server filter using the _or_ operator."""
        return filter_from_url_arg(self.model_cls, query, arg, query_operator=or_)

    def create(self, *args, **kwargs):
        """Adds created http status response and location link."""
        resource = super(JsonServerResource, self).create(*args, **kwargs)

        return ResourceResult(
            body=resource,
            status=get_http_status_code_value(http.client.CREATED),
            location="{}/{}".format(request.url, resource.get_id())
        )

    def _create_filter_by(self):
        """Transform the json-server filter arguments to model-resource ones."""
        filter_by = []

        for name, values in request.args.copy().lists():  # copy.lists works in py2 and py3
            if name not in _SKIPPED_ARGUMENTS:
                column = _re_column_name.search(name).group(1)

                if column not in self._model_columns:
                    continue

                for value in values:
                    if name.endswith('_ne'):
                        filter_by.append(name[:-3] + '!=' + value)
                    elif name.endswith('_lte'):
                        filter_by.append(name[:-4] + '<=' + value)
                    elif name.endswith('_gte'):
                        filter_by.append(name[:-4] + '>=' + value)
                    elif name.endswith('_like'):
                        filter_by.append(name[:-5] + '::like::%' + value + '%')
                    else:
                        filter_by.append(name.replace('__', '.') + '==' + value)

        filter_by += self._create_fulltext_query()

        return ','.join(filter_by)

    @staticmethod
    def _create_related(args):
        # type: (Dict) -> None
        """Create related field from `_embed` arguments."""
        if '_embed' in request.args:
            embeds = request.args.getlist('_embed')

            args['related'] = ','.join(embeds)

            del args['_embed']

    def _create_fulltext_query(self):
        """Support the json-server fulltext search with a broad LIKE filter."""
        filter_by = []

        if 'q' in request.args:
            columns = flat_model(model_tree(self.__class__.__name__, self.model_cls))
            for q in request.args.getlist('q'):
                filter_by += ['{col}::like::%{q}%'.format(col=col, q=q) for col in columns]

        return filter_by

    def _transform_list_args(self, args):
        # type: (dict) -> None
        """Transforms all list arguments from json-server to model-resource ones.

        This modifies the given arguments.
        """

        if '_limit' in args:
            args['limit'] = int(args['_limit'])
            del args['_limit']

        if '_page' in args:
            page = int(args['_page'])
            if page < 0:
                page = 1

            args['page'] = page
            del args['_page']

            if 'limit' not in args:
                args['limit'] = 10

        if '_end' in args:
            end = int(args['_end'])
            args['limit'] = end - int(args.get('_start', 0))

        if '_start' in args:
            args['offset'] = args['_start']
            del args['_start']

        if '_sort' in args:
            args['order_by'] = args['_sort'].replace('__', '.')
            del args['_sort']

            if args.get('_order', 'ASC') == 'DESC':
                args['order_by'] = '-' + args['order_by']

        if '_order' in args:
            del args['_order']

        filter_by = self._create_filter_by()
        if filter_by:
            args['filter_by'] = filter_by

    def read(self, params, args, data):
        """Modifies the parameters and adds metadata for read results."""
        result_count = None
        result_links = None

        if params is None:
            params = []
        if args:
            args = args.copy()
        else:
            args = {}

        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if not row_id:
            self._transform_list_args(args)

            if 'page' in args or 'limit' in args:
                ctx = self._create_context(params, args, data)

                result_count = self._get_collection_count(ctx)

            if 'page' in args:
                result_links = _get_link_pages(
                    page=args['page'],
                    per_page=int(args['limit']),
                    count=result_count,
                    page_url=request.url
                )

            if 'limit' not in args:
                args['limit'] = 'unlimited'

        self._create_related(args)

        try:
            return ResourceResult(
                body=super(JsonServerResource, self).read(params, args, data),
                count=result_count,
                links=result_links
            )
        except NoResultFound:
            return NOT_FOUND

    def update(self, *args, **kwargs):
        """Modifies the parameters and adds metadata for update results.

        Currently it does not support `PUT` method, which works as replacing
        the resource. This is somehow questionable in relation DB.
        """
        if request.method == 'PUT':
            logging.warning("Called not implemented resource method PUT")

        resource = super(JsonServerResource, self).update(*args, **kwargs)

        if resource:
            return resource
        else:
            return NOT_FOUND

    @transactional
    def delete(self, params, args, data):
        """Supports only singular delete and adds proper http status."""
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id:
            deleted = self._delete_one(row_id, ctx)

            if deleted:
                return ResourceResult(body={})
            else:
                return NOT_FOUND
        else:
            return NOT_FOUND
