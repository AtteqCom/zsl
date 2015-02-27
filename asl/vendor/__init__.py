import sys
import os

_vendor_initialized = False

def append_paths(path, vendor_modules):
    new_path = []
    for v in vendor_modules:
        new_path.append(path + os.sep + v)
    sys.path = new_path + sys.path

def do_init():
    global _vendor_initialized
    if _vendor_initialized:
        return

    _vendor_initialized = True

    path = "."
    if os.path.exists('./asl/asl/vendor'):
        path = os.path.abspath('./asl/asl/vendor')
    else:
        for p in sys.path:
            if os.path.exists(p + '/vendor/'):
                path = os.path.abspath(p + '/vendor/')
                break
            if os.path.exists(p + '/asl/vendor/'):
                path = os.path.abspath(p + '/asl/vendor/')
                break

    vendor_modules = ['injector', 'flask_injector', 'redis-py', 'sqlalchemy/sqlalchemy-0_9_1/lib', 'bpython/bpython', 'sphinxapi', 'simplejson']
    append_paths(path, vendor_modules)

do_init()
