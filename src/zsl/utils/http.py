from http import HTTPStatus
from typing import Union


def get_http_status_code_value(status_code):
    # type: (Union[int|HTTPStatus])->int
    """Py2/3 status code."""
    if hasattr(status_code, 'value'):
        return status_code.value  # python 3
    else:
        return status_code  # python 2
