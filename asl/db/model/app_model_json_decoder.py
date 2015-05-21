'''
Created on 8.4.2013

.. moduleauthor:: Martin Babka
'''
from json.decoder import JSONDecoder, WHITESPACE
import importlib

def get_json_decoder(full_class_name):
    class AppModelJSONDecoder(JSONDecoder):
        def decode(self, s, _w=WHITESPACE.match):
            values = JSONDecoder.decode(self, s, _w=_w)
            (module_name, class_name) = full_class_name.rsplit('.', 1)
            module = importlib.import_module(module_name)
            model = getattr(module, class_name)(values)
            return model

    return AppModelJSONDecoder
