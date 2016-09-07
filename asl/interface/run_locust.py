# EASY-INSTALL-ENTRY-SCRIPT: 'locustio==0.7.2','console_scripts','locust'
__requires__ = 'locustio==0.7.2'

from importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

import sys
from pkg_resources import load_entry_point


if __name__ == '__main__':
    sys.exit(
        load_entry_point('locustio==0.7.2', 'console_scripts', 'locust')()
    )
