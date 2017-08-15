"""
:mod:`zsl.db.model.app_model_json_decoder`
------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from json.decoder import WHITESPACE, JSONDecoder

from zsl.utils.import_helper import fetch_class


def get_json_decoder(full_class_name, hints=None):
    class AppModelJSONDecoder(JSONDecoder):
        def decode(self, s, _w=WHITESPACE.match):
            values = JSONDecoder.decode(self, s, _w=_w)
            model = fetch_class(full_class_name)(values, 'id', hints)
            return model

    return AppModelJSONDecoder
