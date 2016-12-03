'''
:mod:`asl.interface.tools.importer`

.. moduleauthor:: Martin Babka
'''

import sys
import os

# TODO: Consider removing automatic path initialization!


def append_asl_path_to_pythonpath():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from zsl.interface.importer import skip_appending_asl_path_to_pythonpath
    skip_appending_asl_path_to_pythonpath()
