from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *


def extract_data(request):
    data = request.data
    json_data = request.get_json()
    return json_data if json_data else data
