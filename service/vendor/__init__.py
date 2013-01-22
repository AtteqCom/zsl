import sys
import os

__vendor_initialized = False

def do_init():
    global __vendor_initialized
    if __vendor_initialized:
        return

    __vendor_initialized = True
    path = os.path.abspath('.')
    if os.path.exists('../../vendor/'):
        path = os.path.abspath('../../vendor/')

    vendor_modules = ['flask_injector', 'injector', 'redis']
    for v in vendor_modules:
        sys.path.append(path + os.sep + v)

do_init()
