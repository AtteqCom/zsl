import sys
import os

_vendor_initialized = False

def do_init():
    global _vendor_initialized
    if _vendor_initialized:
        return

    _vendor_initialized = True
    path = "."
    for p in sys.path:
        if os.path.exists(p + '/vendor/'):
            path = os.path.abspath(p + '/vendor/')
            break
        if os.path.exists(p + '/asl/vendor/'):
            path = os.path.abspath(p + '/asl/vendor/')
            break

    vendor_modules = ['flask_injector', 'injector', 'redis', 'sqlalchemy/sqlalchemy-rel_0_7/lib', 'bpython/bpython']
    for v in vendor_modules:
        sys.path.append(path + os.sep + v)

do_init()
