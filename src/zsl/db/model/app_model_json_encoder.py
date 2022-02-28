"""
:mod:`zsl.db.model.app_model_json_encoder`
------------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

from json.encoder import JSONEncoder

from typing import Any

from zsl.db.model import AppModel
from zsl.interface.dict_into_namedtuple_converter import is_typed_named_tuple_type


class AppModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AppModel):
            return o.get_attributes()
        elif isinstance(o, object):
            return dict(o.__dict__)
        else:
            return JSONEncoder.default(self, o)

    def encode(self, o):
        # type: (Any)->str
        if is_typed_named_tuple_type(type(o)):
            # NOTE: this is a well documented method. The underscore here is to prevent clashes with possible fields,
            # not to mark it as private
            o = o._asdict()

        return super().encode(o)
