'''
:mod:`asl.utils.php_helper`

.. moduleauthor:: Peter Morihladko

Some handy function when dealing with code written in PHP
'''

def bool_to_str(boolean):
    '''
    Convert ``boolean`` to string like PHP 
    '''
    return '1' if boolean else ''