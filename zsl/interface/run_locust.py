"""
:mod:`zsl.interface.run_locust`
-------------------------------
"""
from __future__ import unicode_literals
# EASY-INSTALL-ENTRY-SCRIPT: 'locustio==0.7.2','console_scripts','locust'
__requires__ = 'locustio==0.7.2'

import sys
from pkg_resources import load_entry_point


if __name__ == '__main__':
    sys.exit(
        load_entry_point('locustio==0.7.2', 'console_scripts', 'locust')()
    )
