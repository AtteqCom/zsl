'''
Helper for nginx push stream module
https://github.com/wandenberg/nginx-push-stream-module  
'''

import urllib
import urllib2
import json

class NginxPusher:
    def __init__(self, server_path, channel_prefix=None):
        self._server_path = server_path
        self._channel_prefix = (channel_prefix + '.') if channel_prefix is not None else ''
        
    def channel_path(self, channel_id):
        return '{0}?id={1}{2}'.format(self._server_path, self._channel_prefix, channel_id)

    def push_msg(self, channel_id, msg):
        '''
        Push ``msg`` for given ``channel_id``. If ``msg`` is not string, it will be urlencoded
        '''
        
        if type(msg) is not str:
            msg = urllib.urlencode(msg) 
        
        return self.push(channel_id, msg)
    
    def push_object(self, channel_id, obj):
        '''
        Push ``obj`` for ``channel_id``. ``obj`` will be encoded as JSON in the request.
        '''
        
        return self.push(channel_id, json.dumps(obj).replace('"', '\\"'))
        
    def push(self, channel_id, data):
        '''
        Push message with POST ``data`` for ``channel_id``
        '''
        
        channel_path = self.channel_path(channel_id)
        response = urllib2.urlopen(channel_path, data)
        
        return json.dumps(response.read())
    
    def delete_channel(self, channel_id):
        '''
        Deletes channel
        '''
        req = urllib2.Request(self.channel_path(channel_id))
        req.get_method = lambda: 'DELETE'
        
        response = urllib2.urlopen(req).read()
        
        return response.read()
    
    # TODO channel stats
        
    
    # TODO
    #def get_msg(self, channel_id):
    #    pass
    