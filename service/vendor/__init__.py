import sys
import os

__vendor_initialized = False

def do_init():
    global __vendor_initialized
    if __vendor_initialized:
        return

    __vendor_initialized = True
    path = "."
    for p in sys.path:
        if os.path.exists(p + '/vendor/'):
            path = os.path.abspath(p + '/vendor/')
            break

    vendor_modules = ['flask_injector', 'injector', 'redis', 'sqlalchemy/sqlalchemy-rel_0_7/lib']
    for v in vendor_modules:
        sys.path.append(path + os.sep + v)

do_init()
