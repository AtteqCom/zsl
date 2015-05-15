#!/usr/bin/python

from importer import append_asl_path_to_pythonpath
append_asl_path_to_pythonpath()

from asl.interface.run import run_webapp

if __name__ == "__main__":
    run_webapp()
