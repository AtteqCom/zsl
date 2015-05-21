'''
Created on Dec 13, 2013

.. moduleauthor:: Peter Morihladko
'''
import os, errno

def mkdir_p(path):
    """
    like `mkdir -p path`
    found on stackoverflow
    """
    
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise