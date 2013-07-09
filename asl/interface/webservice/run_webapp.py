#!/usr/bin/python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));

from asl.interface.importer import append_pythonpath
append_pythonpath()
from asl.interface.webservice import web_application_loader
web_application_loader.load()

# Now import the application and the remaining stuff.
from asl.application import service_application
service_application.initialize_dependencies()

def run_shell():
    import bpython
    bpython.embed()

def run_task(args):
    if len(args) == 0:
        raise Exception('I need a task path to run')

def run_webapp():
    service_application.run()

# Run it!
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'shell':
            run_shell()

        elif cmd == 'task':
            run_task(sys.argv[1:])

        else:
            run_webapp()

    else:
        run_webapp()
