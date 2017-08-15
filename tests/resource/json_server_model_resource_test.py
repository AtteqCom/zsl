"""
:mod:`tests.resource.json_server_model_resource`
------------------------------------------------
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import http.client
import json
import math
import re
from resource.resource_test_helper import (UserModel, UserTuple, addresses, create_resource_test_data,
                                           get_non_existent_id, users)
from typing import AnyStr, Dict, List, Optional, Union
from unittest.case import TestCase
import urllib

from future.utils import viewitems

from zsl import Zsl
from zsl.application.containers.web_container import WebContainer
from zsl.resource.json_server_resource import JsonServerResource
from zsl.testing.db import IN_MEMORY_DB_SETTINGS
from zsl.testing.http import HTTPTestCase, json_loads
from zsl.testing.test_utils import parent_module

# py23
if hasattr(urllib, 'parse'):
    urlencode = urllib.parse.urlencode
else:
    urlencode = urllib.urlencode


def parse_links_header(links_str):
    # type: (AnyStr) -> Dict[AnyStr, AnyStr]
    """Parse the link http header including resource metadata.

    :param links_str: link http header
    :type links_str: str
    :return: dictionary where key is the link name and value is the link
    :rtype dict[str, str]
    """

    result = {}
    parts = links_str.split(',')

    for p in parts:
        name = re.search(r'rel="([^"]+)"', p).group(1)
        url = re.search(r'<([^>]+)>', p).group(1)

        result[name] = url

    return result


def parse_page_link_headers(links_str):
    # type: (AnyStr) -> Dict[AnyStr, int]
    """Parse the link http header and get the page position from the links

    :param links_str: link http header
    :type links_str: str
    :return: dictionary where key is the link name and value is the page number
    :rtype: dict[str, int]
    """

    links = parse_links_header(links_str)

    return {
        name: int(re.search(r'_page=([\d]+)', url).group(1))
        for name, url in viewitems(links)
    }


def is_ascending(list_):
    # type: (List[int]) -> bool
    """Test if the list is in an ascending order."""

    try:
        prev = list_[0]
    except IndexError:
        return True

    for i in list_[1:]:
        if prev > i:
            return False
        prev = i
    return True


def is_descending(list_):
    # type: (List[int]) -> bool
    """Test if the list is in an descending order."""

    try:
        prev = list_[0]
    except IndexError:
        return True

    for i in list_[1:]:
        if prev < i:
            return False
        prev = i
    return True


def in_user_address(user_id, q):
    # type: (int, AnyStr) -> bool
    """Test if string is in any address property."""
    return any(a for a in addresses if a.user_id == user_id and (q in str(
        a.id) or q in a.email_address))


def in_user(user, q):
    # type: (UserTuple, AnyStr) -> bool
    """Test if string is in any user property and in its address properties."""
    return q in str(user.id) or q in user.name or in_user_address(user.id, q)


class JsonServerModelResourceTestResource(JsonServerResource):
    """Test resource based on JsonServerResource."""
    __model__ = UserModel


class JsonServerModelResourceTestCase(TestCase, HTTPTestCase):
    PATH = '/resource/json_server_model_resource_test'

    def setUp(self):
        config_object = IN_MEMORY_DB_SETTINGS.copy()
        # add this package as resource package for zsl to find the
        # `JsonServerModelResourceResource`
        config_object['RESOURCE_PACKAGES'] = ('resource',)
        zsl = Zsl(__name__, config_object=config_object,
                  modules=WebContainer.modules())
        zsl.testing = True

        # mock http requests
        self.app = zsl.test_client()

        create_resource_test_data()

    def _path(self, res_id=None, args=None, raw_args=''):
        # type: (Optional[Union[AnyStr, int]], Dict[AnyStr, Union[str, int]], AnyStr) -> str
        """Generate a resource link

        :param res_id: resource id
        :param args: optional url arguments as {name: value}
        :param raw_args: url arguments in string, appended after args
        :return: url path for resource
        """
        if args:
            args = '?' + urlencode(args)
        else:
            args = ''

        if args:
            args += '&' + raw_args
        elif raw_args:
            args = '?' + raw_args

        if res_id:
            return "{path}/{id_}{args}".format(
                path=self.PATH,
                id_=res_id,
                args=args
            )
        else:
            return "{path}{args}".format(
                path=self.PATH,
                args=args
            )

    def testCreate(self):
        user_data = {'name': 'eleven'}

        rv = self.app.post(self.PATH, data=json.dumps(user_data), content_type='application/json')
        user = json_loads(rv.data)

        self.assertEqual(user_data['name'], user['name'])
        self.assertHTTPStatus(http.client.CREATED, rv.status_code, 'http status should be 201')

        rv = self.app.get(rv.location)
        self.assertDictEqual(user, json_loads(rv.data), 'object should be saved')

    def testReadOne(self):
        rv = self.app.get(self._path(res_id=1))

        self.assertDictEqual(users[0]._asdict(), json_loads(rv.data), 'json should equal model value')
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')

    def testReadNotFound(self):
        rv = self.app.get(self._path(res_id=get_non_existent_id()))

        self.assertDictEqual({}, json_loads(rv.data), 'should return empty json')
        self.assertHTTPStatus(http.client.NOT_FOUND, rv.status_code, 'http status should be 404')

    def testUpdateWithPut(self):
        """Put - same as patch."""
        update = {'name': 'eleven'}

        original = users[0]

        rv = self.app.put(self._path(res_id=original.id), data=json.dumps(update), content_type='application/json')
        user = json_loads(rv.data)

        updated = original._asdict()
        updated['name'] = update['name']

        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertDictEqual(updated, user, 'updated value should be returned')

        rv = self.app.get(self._path(res_id=original.id))
        self.assertDictEqual(updated, json_loads(rv.data), 'updated value should be stored')

    def testUpdateWithPatch(self):
        """Patch - update partially."""

        original = users[0]
        update = {'name': 'new value'}

        rv = self.app.patch(self._path(res_id=original.id), data=json.dumps(update), content_type='application/json')
        user = json_loads(rv.data)

        updated = original._asdict()
        updated['name'] = update['name']

        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertDictEqual(updated, user, 'updated value should be returned')

        rv = self.app.get(self._path(res_id=original.id))
        self.assertDictEqual(updated, json_loads(rv.data), 'updated value should be stored')

    def testUpdateWithPatchNotFound(self):
        update = {'name': 'new value'}

        rv = self.app.patch(self._path(res_id=get_non_existent_id()), data=json.dumps(update),
                            content_type='application/json')

        self.assertDictEqual({}, json_loads(rv.data), 'should return empty json')
        self.assertHTTPStatus(http.client.NOT_FOUND, rv.status_code, 'http status should be 404')

    def testDelete(self):
        to_delete = users[0]

        rv = self.app.delete(self._path(res_id=to_delete.id))

        self.assertDictEqual({}, json_loads(rv.data), 'should return empty json')
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')

        rv = self.app.get(self._path(res_id=to_delete.id))
        self.assertDictEqual({}, json_loads(rv.data), 'should be deleted')
        self.assertHTTPStatus(http.client.NOT_FOUND, rv.status_code, 'http status should be 404')

    def testDeleteAll(self):
        rv = self.app.delete(self.PATH)

        self.assertDictEqual({}, json_loads(rv.data), 'should be empty')
        self.assertHTTPStatus(http.client.NOT_FOUND, rv.status_code, 'http status should be 404')

    def testDeleteNotFound(self):
        rv = self.app.delete(self._path(res_id=get_non_existent_id()))

        self.assertDictEqual({}, json_loads(rv.data), 'should be empty')
        self.assertHTTPStatus(http.client.NOT_FOUND, rv.status_code, 'http status should be 404')

    def testReadMany(self):
        rv = self.app.get(self.PATH)
        data = json_loads(rv.data)

        self.assertEqual(len(users), len(data), 'should return all elements')
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')

    def testReadManyWithPageAndDefaultLimit(self):
        page = 1
        default_limit = 10

        rv = self.app.get(self._path(args={'_page': page}))
        data = json_loads(rv.data)

        self.assertEqual(default_limit, len(data), 'should return 10 items')
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

    def testReadManyWithLimit(self):
        limit = 5

        rv = self.app.get(self._path(args={'_limit': limit}))
        data = json_loads(rv.data)

        self.assertEqual(limit, len(data), 'should return %d items' % limit)
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

        count = 3
        offset = len(users) - count
        limit = 5

        rv = self.app.get(self._path(args={'_limit': limit, '_start': offset}))
        data = json_loads(rv.data)

        self.assertEqual(count, len(data), 'should return %d items' % count)
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

    def testReadManyWithPage(self):
        page = 2
        limit = 3

        rv = self.app.get(self._path(args={'_page': page, '_limit': limit}))
        data = json_loads(rv.data)

        self.assertEqual(limit, len(data), 'should return %d items' % limit)
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

        pages = parse_page_link_headers(rv.headers['Links'])
        self.assertEqual(1, pages.get('first'), 'there should be link to first page')
        self.assertEqual(page - 1, pages.get('prev'), 'there should be link to prev page')
        self.assertEqual(page + 1, pages.get('next'), 'there should be link to next page')
        self.assertEqual(math.ceil(len(users) / limit), pages.get('last'),
                         'there should be link to last page')

    def testReadManyWithStartAndEnd(self):
        end = 7

        rv = self.app.get(self._path(args={'_end': end}))
        data = json_loads(rv.data)

        self.assertEqual(end, len(data), 'should return %d items' % end)
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

        start = 3
        end = 10

        rv = self.app.get(self._path(args={'_start': start, '_end': end}))
        data = json_loads(rv.data)

        self.assertEqual(end - start, len(data), 'should return %d items' % (end - start))
        self.assertHTTPStatus(http.client.OK, rv.status_code, 'http status should be 200')
        self.assertEqual(len(users), int(rv.headers['X-Total-Count']),
                         'response header \'X-Total-Count\' should be set')

    def testReadManyWithSort(self):
        rv = self.app.get(self._path(args={'_sort': 'id'}))
        data = json_loads(rv.data)

        self.assertTrue(is_ascending([d['id'] for d in data]), 'default sort direction should be ascend')

        rv = self.app.get(self._path(args={'_sort': 'id', '_order': 'DESC'}))
        data = json_loads(rv.data)

        self.assertTrue(is_descending([d['id'] for d in data]), 'sort direction should be descent')

    def testReadManyWithFilters(self):
        rv = self.app.get(self._path(args={'name': 'nine'}))
        data = json_loads(rv.data)

        expected_length = len([d for d in users if d.name == 'nine'])
        self.assertEqual(expected_length, len(data), 'should filter with help of \'name\' param')

        rv = self.app.get(self._path(raw_args='name=nine&name=seven'))
        data = json_loads(rv.data)

        expected_length = len([d for d in users if d.name == 'nine' or d.name == 'seven'])
        self.assertEqual(expected_length, len(data),
                         'should filter with help of OR operator and supporting multiple key values')

        rv = self.app.get(self._path(raw_args='id_gte={id1}&name={name1}&id_lte={id2}&name_like={name2}'.format(
            id1=len(users), id2=1, name1='seven', name2='eig'
        )))
        data = json_loads(rv.data)

        expected_length = len([d for d in users
                               if d.id <= 1 or d.id >= len(users) or d.name == 'seven' or 'eig' in d.name])
        self.assertEqual(expected_length, len(data),
                         'should filter with help of various operators')

        rv = self.app.get(self._path(args={'not_existent_column': 'x', 'id': 1}))
        data = json_loads(rv.data)

        self.assertEqual(1, len(data), 'should ignore unknown column')

    def testFulltextQuery(self):
        q = '@'

        rv = self.app.get(self._path(args={'q': q}))
        data = json_loads(rv.data)

        expected_length = len([u for u in users if in_user(u, q)])
        self.assertEqual(expected_length, len(data), 'should filter using a fulltext query')

    def testEmbed(self):
        user_id = 1
        rv = self.app.get(self._path(res_id=user_id, args={'_embed': 'addresses'}))
        data = json_loads(rv.data)

        expected_length = len([a for a in addresses if a.user_id == user_id])
        self.assertEqual(expected_length, len(data['addresses']), 'should return user with embedded addresses')

        rv = self.app.get(self._path(args={'_embed': 'addresses', '_sort': 'id', '_page': 1}))
        data = json_loads(rv.data)

        for u in data:
            expected_length = len([a for a in addresses if a.user_id == u['id']])
            self.assertEqual(expected_length, len(u['addresses']), 'should return users with embedded addresses')
