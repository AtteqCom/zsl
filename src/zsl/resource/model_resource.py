"""
:mod:`zsl.resource.model_resource` -- REST for a DB model.
----------------------------------------------------------

Resources provide a way how to directly access DB tables (raw models) and
perform CRUD operations upon them. The default classes of the models should be
overridden to provide more logic or restrictions if wanted.

The basic way to use them is as follows:
 - The models can be defined in the __exposer__.py which is set up at settings.
 - To override just override the basic methods - `create`, `read`, `update`,
   `delete`.

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

from builtins import int, object
from hashlib import sha256
import json
import logging
from typing import Any, List, Union

from future.utils import viewitems
from sqlalchemy.orm import class_mapper

from zsl import inject
from zsl.cache.cache_module import CacheModule
from zsl.cache.id_helper import IdHelper, create_key_class_prefix
from zsl.db.helpers import app_models
from zsl.db.helpers.nested import nested_model, nested_models
from zsl.db.model.app_model import AppModel
from zsl.resource.resource_helper import (apply_related, create_related_tree, filter_from_url_arg, order_from_url_arg,
                                          related_from_fields)
from zsl.service.service import TransactionalSupportMixin, transactional
from zsl.utils.cache_helper import app_model_decoder_fn, app_model_encoder_fn


def dict_pick(dictionary, allowed_keys):
    """
    Return a dictionary only with keys found in `allowed_keys`
    """
    return {key: value for key, value in viewitems(dictionary) if key in allowed_keys}


def page_to_offset(params):
    """
    Transforms `page`/`per_page` from `params` to `limit`/`offset` suitable for SQL.

    :param dict params: The dictionary containing `page` and `per_page` values will be added
                        the values `limit` and `offset`.
    """

    if 'page' not in params:
        return

    page = params['page']
    del params['page']

    # 'per_page' je len alias za 'limit'
    if 'per_page' in params:
        per_page = params.get('per_page')
        del params['per_page']
    else:
        per_page = params.get('limit', 10)

    params['offset'] = int(per_page) * (int(page) - 1)
    params['limit'] = per_page


def _is_list(list_):
    # type: (Any) -> bool
    """Test if variable is a list.

    Maybe this is not the best way to test for a list, but it is sufficient for
    current use case.
    """
    try:
        len(list_)
        return True
    except TypeError:
        return False


class ResourceQueryContext(object):
    """
    The context of the resource query.
     - holds the parameters and arguments of the query,
     - holds the related models which should be fetched (parsed from the arguments),
     - holds the given filter and splits it to the given field array (parsed from the arguments)

    .. automethod:: __init__
    """

    def __init__(self, params, args, data):
        # type: (dict, list, dict) -> ()
        self._args = args.copy()
        self._args_original = args
        self._data = data

        self._params = params if _is_list(params) else [params]

        # Prepare fields and related.
        if 'related' in self._args:
            self._args['related'] = self._args['related'].split(',')

        if 'fields' in self._args:
            self._args['fields'] = self._args['fields'].split(',')
            # we can pass related fields with this, ensure its in 'related' union of two lists
            self._args['related'] = list(
                set(self._args.get('related', [])) | set(related_from_fields(self._args['fields'])))

    @property
    def params(self):
        """Params are given as the part of the path in URL. For example GET /entities/1 will have.
        1 in the params.
        """
        return self._params

    @property
    def args(self):
        """Args are in the query part of the url ?related=&filter_by etc."""
        return self._args

    @property
    def data(self):
        """Body of the request."""
        return self._data

    def get_row_id(self):
        """First parameter, if given, else None. Handy for GET requests."""
        return None if len(self.params) == 0 else self.params[0]

    def get_related(self):
        """Related argument - parsed as array, original argument containing the
        list of comma delimited models which should be fetched along with the resource.
        """
        return self._args.get('related', None)

    def get_filter_by(self):
        """Filter argument - list of filters."""
        return self._args.get('filter_by', None)


class ModelResourceBase(TransactionalSupportMixin):
    """ModelResource works only for tables with a single-column identifier
    (key).

    .. automethod:: __init__
    """

    def __init__(self, model_cls=None):
        """
        Create Model CRUD resource for ``model_cls``
        """

        super(ModelResourceBase, self).__init__()

        if not model_cls:
            self.model_cls = self.__model__
        else:
            self.model_cls = model_cls

        mapper = class_mapper(self.model_cls)
        self._model_pk = mapper.primary_key[0]
        self._model_columns = [column.key for column in mapper.column_attrs]
        self._related_columns = [column.key for column in mapper.relationships]

    def to_filter(self, query, arg):
        return filter_from_url_arg(self.model_cls, query, arg)

    def add_related(self, query, related):
        return apply_related(self.model_cls, query, related)

    def set_ordering(self, query, arg):
        return order_from_url_arg(self.model_cls, query, arg)


class ModelResource(ModelResourceBase):
    """

    .. automethod:: _create_context
    .. automethod:: _create_one
    .. automethod:: _save_one
    .. automethod:: _delete_one
    .. automethod:: _create_delete_one_query
    """
    @staticmethod
    def _create_context(params, args, data):
        # type: (dict, list, dict) -> ResourceQueryContext
        """
        Creates the resource query context - this an object holding the data
        alongside the querying of the resource. This object is always present as
        a parameter for each method during the query and users.py are free to
        create own properties so that they can optimize and perform the query
        (so the subsequent methods have an access to the already precomputed
        data).
        """
        return ResourceQueryContext(params, args, data)

    @transactional
    def create(self, params, args, data):
        # type: (str, dict, dict) -> AppModel
        """
        POST /resource/model_cls/
        data

        Create new resource
        """
        ctx = self._create_context(params, args, data)
        model = self._create_one(ctx)
        self._save_one(model, ctx)
        return self._return_saved_one(model, ctx)

    def read(self, params=None, args=None, data=None):
        # type: (str, dict, dict) -> Union[List[AppModel], AppModel]
        """
        GET /resource/model_cls/[params:id]?[args:{limit,offset,page,per_page,filter_by,order_by,related,fields}]

        Get resource/s

        :param params
        :type params list
        :param args
        :type args dict
        :param data
        :type data: dict
        """
        if params is None:
            params = []
        if args is None:
            args = {}

        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id:
            return self._get_one(row_id, ctx)

        elif 'count' in args:
            return self._get_collection_count(ctx)

        elif 'desc' in args:
            return self._get_collection_desc(ctx)

        else:
            if 'page' in ctx.args:
                page_to_offset(ctx.args)

            return self._get_collection(ctx)

    @transactional
    def update(self, params, args, data):
        # type: (str, dict, dict) -> Union[List[AppModel], AppModel]
        """
        PUT /resource/model_cls/[params:id]
        data

        Update resource/s
        """
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id is not None:
            model = self._update_one(ctx)
            return None if model is None else model.get_app_model()
        else:
            return app_models(self._update_collection(ctx))

    @transactional
    def delete(self, params, args, data):
        # type: (str, dict, dict) -> None
        """
        DELETE /resource/model_cls/[params]?[args]

        delete resource/s
        """
        ctx = self._create_context(params, args, data)
        row_id = ctx.get_row_id()

        if row_id is not None:
            return self._delete_one(row_id, ctx)
        else:
            return self._delete_collection(ctx)

    # Create implementation
    def _create_one(self, ctx):
        """
        Creates an instance to be saved when a model is created.
        """
        assert isinstance(ctx, ResourceQueryContext)

        fields = dict_pick(ctx.data, self._model_columns)
        model = self.model_cls(**fields)
        return model

    def _save_one(self, model, ctx):
        """
        Saves the created instance.
        """
        assert isinstance(ctx, ResourceQueryContext)

        self._orm.add(model)
        self._orm.flush()

    @staticmethod
    def _return_saved_one(model, ctx):
        """
        Returns the result of the create operation.
        """
        return model.get_app_model()

    # Read one implementation.
    @transactional
    def _get_one(self, row_id, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        q = self._orm.query(self.model_cls).filter(self._model_pk == row_id)

        related = ctx.get_related()
        if related is not None:
            q = self.add_related(q, related)
            return nested_model(self._read_one(q, ctx),
                                create_related_tree(related))
        else:
            return self._read_one(q, ctx).get_app_model()

    @staticmethod
    def _read_one(q, ctx):
        return q.one()

    # Read collection implementation.
    def _create_collection_query(self, ctx):
        return self._orm.query(self.model_cls)

    @transactional
    def _get_collection_count(self, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        filter_by = ctx.get_filter_by()

        q = self._create_collection_query(ctx)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return self._read_collection_count(q, ctx)

    def _read_collection_count(self, q, ctx):
        return q.with_entities(self._model_pk).count()

    @transactional
    def _get_collection(self, ctx):
        assert isinstance(ctx, ResourceQueryContext)

        order_by = ctx.args.get('order_by', None)
        filter_by = ctx.get_filter_by()
        related = ctx.get_related()

        q = self._create_collection_query(ctx)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        if order_by is not None:
            q = self.set_ordering(q, order_by)

        if related is not None:
            q = self.add_related(q, related)
            return nested_models(self._read_collection(q, ctx),
                                 create_related_tree(related))
        else:
            return app_models(self._read_collection(q, ctx))

    @staticmethod
    def _read_collection(q, ctx):
        offset = int(ctx.args.get('offset', 0))
        limit = ctx.args.get('limit', 10)
        if limit is not None and limit != 'unlimited':
            q = q.limit(int(limit))
        if offset > 0:
            q = q.offset(offset)
        return q.all()

    def _get_collection_desc(self):
        return [column.name for column in class_mapper(self.model_cls).columns]

    # Update
    def _update_one_simple(self, row_id, fields, ctx):
        fields = dict_pick(fields, self._model_columns)

        model = self._orm.query(self.model_cls).get(row_id)

        if model is None:
            return None

        for name, value in viewitems(fields):
            setattr(model, name, value)

        return model

    def _update_one(self, ctx):
        """
        Update row
        """
        assert isinstance(ctx, ResourceQueryContext)
        fields = ctx.data
        row_id = ctx.get_row_id()
        return self._update_one_simple(row_id, fields, ctx)

    def _update_collection(self, ctx):
        """
        Bulk update
        """
        assert isinstance(ctx, ResourceQueryContext)
        models = []

        for row in ctx.data:
            models.append(self._update_one_simple(row.pop('id'), row, ctx))

        return models

    # Delete methods
    def _delete_one(self, row_id, ctx):
        """
        Deletes row by the given id -- `row_id`. The method first created the
        query using the method :meth:`_create_delete_one_query` and then executes it.

        :param int row_id: Identifier of the deleted row.
        :param ResourceQueryContext ctx: The context of this delete query.
        """
        return self._create_delete_one_query(row_id, ctx).delete()

    def _create_delete_one_query(self, row_id, ctx):
        """
        Delete row by id query creation.

        :param int row_id: Identifier of the deleted row.
        :param ResourceQueryContext ctx: The context of this delete query.
        """

        assert isinstance(ctx, ResourceQueryContext)
        return self._orm.query(self.model_cls).filter(self._model_pk == row_id)

    def _delete_collection(self, ctx):
        """
        Delete a collection from DB, optionally filtered by ``filter_by``
        """
        assert isinstance(ctx, ResourceQueryContext)

        filter_by = ctx.get_filter_by()
        q = self._orm.query(self.model_cls)

        if filter_by is not None:
            q = self.to_filter(q, filter_by)

        return q.delete()


class CachedModelResource(ModelResource):
    """
    The cached resource - uses redis to cache the resource for the given amount of seconds.
    """

    @inject(cache_module=CacheModule, id_helper=IdHelper, logger=logging.Logger)
    def __init__(self, model_cls, cache_module, id_helper, logger, timeout='short'):
        super(CachedModelResource, self).__init__(model_cls)
        self._cache_module = cache_module
        self._id_helper = id_helper
        self._logger = logger
        self._timeout = timeout

    def _create_key(self, arghash):
        key_prefix = create_key_class_prefix(self.model_cls)
        return "cached-resource:{0}:{1}".format(key_prefix, arghash)

    def _create_key_from_context(self, ctx):
        arghash = sha256(json.dumps({'params': ctx.params, 'args': ctx.args, 'data': ctx.data})).hexdigest()
        return self._create_key(arghash)

    def _get_one(self, row_id, ctx):
        # Make hash of params, args and data and ache using the hash in the key.
        key = self._create_key_from_context(ctx)
        self._logger.debug("CachedModelResource - get one, key: {0}.".format(key))

        if self._id_helper.check_key(key):
            result = json.loads(self._id_helper.get_key(key))
        else:
            self._logger.debug("CachedModelResource - get one not cached, transferring to resource...")
            result = super(CachedModelResource, self)._get_one(row_id, ctx)
            # serialize as model
            self._id_helper.set_key(key, app_model_encoder_fn(result), self._timeout)

        self.invalidate()

        return result

    def _get_collection_count(self, ctx):
        # Make hash of params, args and data and ache using the hash in the key.
        key = self._create_key_from_context(ctx)
        self._logger.debug("CachedModelResource - get one, key: {0}.".format(key))

        if self._id_helper.check_key(key):
            result = int(self._id_helper.get_key(key))
        else:
            self._logger.debug("CachedModelResource - get one not cached, transferring to resource...")
            result = super(CachedModelResource, self)._get_collection_count(ctx)
            self._id_helper.set_key(key, app_model_encoder_fn(result), self._timeout)

        return result

    def _get_collection(self, ctx):
        # Make hash of params, args and data and ache using the hash in the key.
        key = self._create_key_from_context(ctx)
        self._logger.debug("CachedModelResource - collection, key: {0}.".format(key))

        if self._id_helper.check_key(key):
            result = self._id_helper.gather_page(key, app_model_decoder_fn)
        else:
            self._logger.debug("CachedModelResource - collection not cached, transferring to resource...")
            result = super(CachedModelResource, self)._get_collection(ctx)
            self._id_helper.fill_page(key, result, self._timeout, app_model_encoder_fn)

        return result

    def invalidate(self):
        """
        Invalidates all the data associated with this model
        """
        key = self._create_key("")
        self._id_helper.invalidate_keys_by_prefix(key)

    def create(self, params, args, data):
        rv = ModelResource.create(self, params, args, data)
        self.invalidate()
        return rv

    def update(self, params, args, data):
        rv = ModelResource.update(self, params, args, data)
        self.invalidate()
        return rv

    def delete(self, params, args, data):
        rv = ModelResource.delete(self, params, args, data)
        self.invalidate()
        return rv


class ReadOnlyResourceUpdateOperationException(Exception):
    def __init__(self, operation):
        self._operation = operation
        super(ReadOnlyResourceUpdateOperationException, self).__init__(
            "Can not perform operation '{0}' on ReadOnlyResource.".format(operation))

    def get_operation(self):
        return self._operation

    operation = property(get_operation)


class ReadOnlyResourceMixin(object):
    """
    The mixin to be used to forbid the update/delete and create operations.
    Remember the Python's MRO and place this mixin at the right place in the inheritance declaration.

    .. automethod:: create
    .. automethod:: update
    .. automethod:: delete
    """

    OPERATION_CREATE = 'create'
    OPERATION_UPDATE = 'update'
    OPERATION_DELETE = 'delete'

    @staticmethod
    def create(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_CREATE)

    @staticmethod
    def update(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_UPDATE)

    @staticmethod
    def delete(params, args, data):
        """Raises exception.

        Just raises ReadOnlyResourceUpdateOperationException to indicate
        that this method is not available.

        :raises ReadOnlyResourceUpdateOperationException: when accessed
        """
        raise ReadOnlyResourceUpdateOperationException(ReadOnlyResourceMixin.OPERATION_DELETE)
