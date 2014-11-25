#!/usr/bin/python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'));

from asl.interface.importer import append_pythonpath
append_pythonpath()
from asl.interface.webservice import web_application_loader

# Now import the application and the remaining stuff.
from asl.application import service_application
service_application.initialize_dependencies()
web_application_loader.load()

conf = service_application.config

def run_shell():
    import bpython
    bpython.embed()

def run_task(args):
    if len(args) == 0:
        raise Exception('I need a task path to run')

def run_webapp():
    service_application.run(
	host=conf.get('FLASK_HOST', '127.0.0.1'),
        port=conf.get('FLASK_PORT'),
        debug=conf.get('DEBUG', False),
        use_debugger=conf.get('USE_DEBUGGER', False),
        use_reloader=conf.get('USE_RELOADER', False)
    )

# Run it!
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == 'shell':
        run_shell()

    elif cmd == 'task':
        run_task(sys.argv[1:])

    elif cmd == 'web':
        run_webapp()

    else:
        print >> sys.stderr, "Usage: run_webappy.py <command>. You provided no or onvalid command - choose one from 'shell', 'task' or 'web'."
