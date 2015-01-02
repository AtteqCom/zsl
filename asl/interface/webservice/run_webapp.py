#!/usr/bin/python

import sys
import os
from asl.interface.run import run_webapp

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));

if __name__ == "__main__":
    run_webapp()
