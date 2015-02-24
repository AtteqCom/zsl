#!/usr/bin/python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));
from asl.interface.run import run_webapp

if __name__ == "__main__":
    run_webapp()
