'''
:mod:`asl.utils.request_helper`

.. moduleauthor:: Martin Babka
'''

def args_to_dict(args):
    '''
    Converts request arguments to a simple dictionary. Uses only the first value.
    '''
    return dict((key, value[0]) for key, value in dict(args).items())