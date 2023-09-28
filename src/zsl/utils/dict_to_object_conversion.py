from datetime import date, datetime
from typing import Any, Dict, Union

from zsl.utils.date_helper import format_date_portable, format_datetime_portable

DATE_DATA = 'date_data'
DATETIME_DATA = 'datetime_data'
RELATED_FIELDS = 'related_fields'
RELATED_FIELDS_CLASS = 'cls'
RELATED_FIELDS_HINTS = 'hints'


def extend_object_by_dict(target, dict_data, hints=None):
    """
    Extends the target object with data from the provided dictionary, using hints to handle specific data types
    and related objects.

    :param target: The object to extend with data from the dictionary.
    :type target: object
    :param dict_data: The dictionary containing data to extend the target object with.
    :type dict_data: dict
    :param hints: A dictionary containing hints on how to handle specific fields.
                  The hints should be organized in the following way::

                      {
                          'date_data': {
                              'field_name': 'date_format',
                              ...
                          },
                          'datetime_data': {
                              'field_name': 'datetime_format',
                              ...
                          },
                          'related_fields': {
                              'field_name': {
                                  'cls': RelatedClass,
                                  'hints': {
                                      'date_data': {...},
                                      'datetime_data': {...},
                                      'related_fields': {...}
                                  }
                              },
                              ...
                          }
                      }

                  The 'date_data' and 'datetime_data' keys contain dictionaries with field names as keys and date or
                  datetime formats as values. This helps to correctly parse date and datetime strings in the provided
                  dictionary.
                  The 'related_fields' key contains a dictionary with field names as keys and dictionaries as values.
                  Each dictionary should have a 'cls' key, which should be a related class, and an optional 'hints'
                  key containing another hints dictionary, used for nested related objects.
    :type hints: dict, optional
    :return: None. The function modifies the target object in-place.
    """
    hints = _get_hints(hints)

    for field_name, field_value in dict_data.items():
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
