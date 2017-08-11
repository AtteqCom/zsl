CORS_CONFIGURATION_NAME = 'CORS'


class CORSConfiguration(object):
    DEFAULT_ALLOW_HEADERS = ['Accept', 'Origin', 'Content-Type', 'Authorization']
    DEFAULT_EXPOSE_HEADERS = ['Location', 'X-Total-Count', 'Link']

    def __init__(self, origin='', allow_headers=None, expose_headers=None):
        # type: (str, Union[List[str], str], Union[List[str], str])->None

        if allow_headers is None:
            allow_headers = self.DEFAULT_ALLOW_HEADERS

        if expose_headers is None:
            expose_headers = self.DEFAULT_EXPOSE_HEADERS

        self._origin = origin
        self._allow_headers = allow_headers
        self._expose_headers = expose_headers

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
