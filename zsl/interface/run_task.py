"""
:mod:`zsl.interface.run_task`
-----------------------------
"""
from __future__ import print_function
from __future__ import unicode_literals
import sys
import os
# TODO: Consider removing automatic path initialization!
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from zsl.interface.run import task

# Run it!
if __name__ == "__main__":
    print(task(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
