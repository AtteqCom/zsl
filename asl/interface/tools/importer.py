'''
Created on 18.5.2015

.. moduleauthor:: Martin Babka
'''

import sys
import os

def append_asl_path_to_pythonpath():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from asl.interface.importer import skip_appending_asl_path_to_pythonpath
    skip_appending_asl_path_to_pythonpath()
