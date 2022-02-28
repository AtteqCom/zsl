from __future__ import absolute_import, division, print_function, unicode_literals

import decimal
import enum
import io
from builtins import *  # NOQA
from builtins import Exception, super, property
from typing import Dict, Type, TypeVar, Union, Tuple, T

from PIL import Image
from future.builtins import str


class ModelConversionError(Exception):
    def __init__(self, message, obj, attribute):
        super(ModelConversionError, self).__init__(message)
        self._obj = obj
        self._attribute = attribute

    @property
    def obj(self):
        return self._obj

    @property
    def attribute(self):
        return self._attribute


def is_typed_named_tuple_type(model_type):
    # type: (Type)->bool
    model_type_bases = model_type.__bases__
    # namedtuple creates instances which inherit from `tuple` only
    if len(model_type_bases) != 1 or model_type_bases[0] != tuple:
        return False

    # namedtuple instances contain field `_fields` with the list of the field names (as strings)
    field_names = getattr(model_type, '_fields', None)
    if not isinstance(field_names, tuple):
        return False

    field_names_are_strings = all(type(field_name) == str for field_name in field_names)
    if not field_names_are_strings:
        return False

    # NamedTuple instances contains also `__annotations__` field, which is a dictionary of field names to types
    annotations = getattr(model_type, '__annotations__', None)
    if not isinstance(annotations, dict):
        return False

    return True


class DictIntoNamedTupleConverter:
    T = TypeVar('T')

    def convert(self, payload, model_type):
        # type: (Dict[str, any], T)->T
        if not is_typed_named_tuple_type(model_type):
            raise Exception(f"The provided model is not NamedTuple: {model_type}")

        annotations: Dict[str, Type] = getattr(model_type, '__annotations__')

        model_fields = set()
        init_kwargs = {}
        for field_name, field_type in annotations.items():
            model_fields.add(field_name)

            if field_name not in payload:
                if self._is_field_optional(field_type):
                    init_kwargs[field_name] = None
                    continue
                elif field_name in model_type._field_defaults.keys():
                    init_kwargs[field_name] = model_type._field_defaults[field_name]
                    continue
                else:
                    raise ModelConversionError(f"Field {field_name} is missing in the request", payload, field_name)

            payload_value = payload[field_name]
            if not self._is_type(payload_value, field_type):
                raise ModelConversionError(
                    f"Expected '{field_name}' to be {field_type}, but is {type(payload_value)}", payload, field_name
                )

            payload_value = self._convert_to_type(payload_value, field_type)
            init_kwargs[field_name] = payload_value

        payload_fields = payload.keys()
        payload_fields_not_in_model_fields = payload_fields - model_fields
        if len(payload_fields_not_in_model_fields) > 0:
            unknown_field_names = ', '.join(payload_fields_not_in_model_fields)
            raise ModelConversionError(
                f"The request contains unknown fields: {unknown_field_names}", payload, unknown_field_names
            )

        return model_type(**init_kwargs)

    def _is_field_optional(self, field_type):
        # type: (Tuple[Type])->bool
        if not hasattr(field_type, '__args__') and not hasattr(field_type, '__origin__'):
            return False

        if field_type.__origin__ is not Union:
            return False

        # typings.Union has __args__ field which is a tuple of all possible fields.
        # Union type is generated also for Optional[xxx] types
        return type(None) in field_type.__args__

    def _is_type(self, value, typehint):
        # type: (any, Type)->bool
        if typehint in [type(None), str, int, float, bool]:
            return type(value) == typehint
        elif typehint == decimal.Decimal:
            return type(value) == float or type(value) == int or type(value) == decimal.Decimal
        elif typehint == Image.Image:
            return type(value) == bytes
        elif self._is_enum_type(typehint):
            return value in set(item.value for item in typehint)
        elif not hasattr(typehint, '__origin__'):
            raise Exception(f"Unsupported typehint for field: {typehint}")
        elif typehint.__origin__ is Union:
            return type(value) in typehint.__args__
        elif typehint.__origin__ is list:
            inner_type_hints = typehint.__args__
            if len(inner_type_hints) > 1:
                raise TypeError(f"Too many inner types for list: {len(typehint.__args__)}")

            if len(inner_type_hints) == 1 and inner_type_hints[0] is T:
                raise TypeError(f"Missing inner type for list")

            if type(value) is not list:
                return False

            inner_type = inner_type_hints[0]
            for list_item in value:
                if not self._is_type(list_item, inner_type):
                    return False

            return True
        else:
            raise Exception(f"Unsupported typehint for field: {typehint}")

    def _is_enum_type(self, typehint: Type) -> bool:
        try:
            return issubclass(typehint, enum.Enum)
        except TypeError:
            return False

    def _convert_to_type(self, value, typehint):
        # type: (any, Type)->any
        if typehint in [type(None)]:
            return None
        elif typehint in [str, int, float, bool]:
            return typehint(value)
        elif typehint == decimal.Decimal:
            return decimal.Decimal(value)
        elif typehint == Image.Image:
            return Image.open(io.BytesIO(value))
        elif self._is_enum_type(typehint):
            return typehint(value)
        elif hasattr(typehint, '__origin__') and typehint.__origin__ is Union and len(typehint.__args__) == 2 and typehint.__args__[1] in [type(None)]:
            return self._convert_to_type(value, typehint.__args__[0])
        else:
            return value
