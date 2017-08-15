from typing import List, Union

CORS_CONFIGURATION_NAME = 'CORS'


class CORSConfiguration(object):
    DEFAULT_ALLOW_HEADERS = ['Accept', 'Origin', 'Content-Type',
                             'Authorization']
    DEFAULT_EXPOSE_HEADERS = ['Location', 'X-Total-Count', 'Link']
    DEFAULT_MAX_AGE = 21600

    def __init__(self, origin='', allow_headers=None, expose_headers=None,
                 max_age=DEFAULT_MAX_AGE):
        # type: (str, Union[List[str], str], Union[List[str], str], int)->None

        if allow_headers is None:
            allow_headers = self.DEFAULT_ALLOW_HEADERS

        if expose_headers is None:
            expose_headers = self.DEFAULT_EXPOSE_HEADERS

        self._origin = origin
        self._allow_headers = allow_headers
        self._expose_headers = expose_headers
        self._max_age = max_age

    @property
    def origin(self):
        # type: ()->str
        return self._origin

    @property
    def allow_headers(self):
        # type: ()->Union[List[str], str]
        return self._allow_headers

    @property
    def expose_headers(self):
        # type: ()->Union[List[str], str]
        return self._expose_headers

    @property
    def max_age(self):
        # type: ()->int
        return self._max_age
