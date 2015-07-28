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

    path = os.path.dirname(__file__)
    vendor_modules = ['injector', 'flask_injector', 'redis-py', 'sqlalchemy/sqlalchemy-0_9_1/lib', 'bpython/bpython', 'sphinxapi', 'simplejson']
    append_paths(path, vendor_modules)

do_init()
