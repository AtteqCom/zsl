"""
:mod:`zsl.interface.resource`
-----------------------------

Helper types describing resource results for resource router.
"""
from collections import namedtuple

result_fields = ['body', 'count', 'links', 'status', 'location', 'expose_headers']

ResourceResult = namedtuple('ResourceResult', result_fields)
ResourceResult.__new__.__defaults__ = (None,) * len(ResourceResult._fields)  # allow creating an empty result
