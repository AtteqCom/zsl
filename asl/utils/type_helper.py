'''
:mod:`asl.utils.type_helper`

.. moduleauthor:: peter
'''

def not_empty_list(l):
    return isinstance(l, list) and len(l) > 0