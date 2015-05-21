#!/usr/bin/python

'''
:mod:`asl.interface.run`

.. moduleauthor:: Peter Morihladko, Martin Babka
'''

# Initialize
from .importer import initialize_web_application
initialize_web_application()

import sys
import json
from asl.router import task_router
from asl.task.job_context import JobContext
from asl.application import service_application

conf = service_application.config


class Job():
    def __init__(self, data):
        self.data = {'data': data}


def run_task(task, data = None):
    if not isinstance(data, str) and not isinstance(data, unicode):
        data = json.dumps(data)
    # Open the data from file, if necessary.
    elif data is not None and data.startswith("file://"):
        with open(data[len("file://"):]) as f:
            data = f.read()

    # Prepare the task.
    job = Job(data)
    (task, task_callable) = task_router.route(task)
    jc = JobContext(job, task, task_callable)
    JobContext.set_current_context(jc)

    # Run the task.
    return jc.task_callable(jc.task_data)


def run_shell():
    import bpython
    bpython.embed()


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
        run_task(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    elif cmd == 'web':
        run_webapp()

    else:
        print >> sys.stderr, "Usage: run_webappy.py <command>. You provided no or invalid command - choose one from 'shell', 'task' or 'web'."
