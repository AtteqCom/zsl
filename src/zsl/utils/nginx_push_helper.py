"""
:mod:`zsl.utils.nginx_push_helper`
----------------------------------

Helper for nginx push stream module
https://github.com/wandenberg/nginx-push-stream-module
"""
from __future__ import unicode_literals

from builtins import object
import json

import requests

from zsl.utils.url_helper import urlencode


class NginxPusher(object):
    def __init__(self, server_path, channel_prefix=None):
        self._server_path = server_path
        self._channel_prefix = (channel_prefix + '.') if channel_prefix is not None else ''

    def channel_path(self, channel_id):
        return '{0}?id={1}{2}'.format(self._server_path, self._channel_prefix, channel_id)

    def push_msg(self, channel_id, msg):
        """Push ``msg`` for given ``channel_id``. If ``msg`` is not string, it
         will be urlencoded
        """

        if type(msg) is not str:
            msg = urlencode(msg)

        return self.push(channel_id, msg)

    def push_object(self, channel_id, obj):
        """Push ``obj`` for ``channel_id``. ``obj`` will be encoded as JSON in
        the request.
        """

        return self.push(channel_id, json.dumps(obj).replace('"', '\\"'))

    def push(self, channel_id, data):
        """Push message with POST ``data`` for ``channel_id``
        """

        channel_path = self.channel_path(channel_id)
        response = requests.post(channel_path, data)

        return response.json()

    def delete_channel(self, channel_id):
        """Deletes channel
        """
        req = requests.delete(self.channel_path(channel_id))
        return req

        # TODO channel stats

        # TODO
        # def get_msg(self, channel_id):
        #    pass
