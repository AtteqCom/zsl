'''
Created on 28.3.2013

@author: Martin Babka
'''

import os
import sys

def append_application_pythonpath():
    app_package_path = os.environ.get('APPLICATION_PACKAGE_PATH')
    if app_package_path is None:
        raise Exception("Application path is not set. Set it using the APPLICATION_PACKAGE_PATH environment variable.")

    sys.path.append(app_package_path)

def append_pythonpath():
    append_application_pythonpath()
