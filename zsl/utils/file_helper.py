"""
:mod:`zsl.utils.file_helper`
----------------------------

.. moduleauthor:: Peter Morihladko <morihladko@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals
import os
import errno


def makedirs(path):
    """Behaves like `mkdir -p <path>`. Without failure if the path exists."""
    
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
