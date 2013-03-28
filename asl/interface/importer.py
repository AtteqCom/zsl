'''
Created on 28.3.2013

@author: Martin Babka
'''

import os
import sys

def append_application_pythonpath():
    sys.path.append(os.environ.get('APPLICATION_PACKAGE_PATH'))

def append_pythonpath():
    append_application_pythonpath()
