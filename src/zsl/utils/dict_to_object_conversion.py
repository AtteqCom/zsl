from __future__ import unicode_literals

# noinspection PyCompatibility
from builtins import int, str
from datetime import date, datetime
from typing import Any, Dict, Union

from future.utils import viewitems

from zsl.utils.date_helper import format_date_portable, format_datetime_portable

DATE_DATA = 'date_data'
DATETIME_DATA = 'datetime_data'
RELATED_FIELDS = 'related_fields'
RELATED_FIELDS_CLASS = 'cls'
RELATED_FIELDS_HINTS = 'hints'


def extend_object_by_dict(target, dict_data, hints=None):
    hints = _get_hints(hints)

    for field_name, field_value in viewitems(dict_data):
        if isinstance(field_value, (type(None), str, int, float, bool)):
            if field_name in hints[DATE_DATA] and field_value is not None:
                d = datetime.strptime(field_value,
                                      hints[DATE_DATA][field_name]).date()
                setattr(target, field_name, format_date_portable(d))
            elif field_name in hints[DATETIME_DATA] and \
                    field_value is not None:
                d = datetime.strptime(field_value,
                                      hints[DATETIME_DATA][field_name])
                setattr(target, field_name, format_datetime_portable(d))
            else:
                setattr(target, field_name, field_value)
        elif isinstance(field_value, datetime):
            setattr(target, field_name, format_datetime_portable(field_value))
        elif isinstance(field_value, date):
            setattr(target, field_name, format_date_portable(field_value))
        elif field_name in hints[RELATED_FIELDS]:
            related_cls = hints[RELATED_FIELDS][field_name][
                RELATED_FIELDS_CLASS]
            related_hints = hints[RELATED_FIELDS][field_name].get(
                RELATED_FIELDS_HINTS)
            if isinstance(field_value, (list, tuple)):
                setattr(
                    target,
                    field_name,
                    [
                        related_cls(_to_dict(x), 'id', related_hints)
                        for x in field_value
                    ]
                )
            else:
                setattr(
                    target,
                    field_name,
                    related_cls(_to_dict(field_value), 'id', related_hints)
                )
        elif isinstance(field_value, (list, tuple)):
            setattr(target, field_name, [x for x in field_value])


def _to_dict(val):
    # type: (Union[Dict[str, Any], object]) -> Dict[str, Any]
    return val if isinstance(val, dict) else val.__dict__


def _get_hints(original_hints):
    if original_hints is None:
        correct_hints = {DATE_DATA: {}, DATETIME_DATA: {}, RELATED_FIELDS: {}}
    else:
        correct_hints = original_hints
        if DATE_DATA not in correct_hints:
            correct_hints[DATE_DATA] = {}
        if DATETIME_DATA not in correct_hints:
            correct_hints[DATETIME_DATA] = {}
        if RELATED_FIELDS not in correct_hints:
            correct_hints[RELATED_FIELDS] = {}

    return correct_hints
