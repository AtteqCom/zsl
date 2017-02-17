"""
:mod:`zsl.interface.celery.run_worker`
---------------------------------------

.. moduleauthor:: Peter Morihladko
"""
from __future__ import print_function
from __future__ import unicode_literals

# Initialize app
from zsl.interface.importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

from zsl.interface.celery.worker import TaskQueueWorker


def main():
    print("Initializing Gearman worker.")
    w = TaskQueueWorker()
    w.run()

if __name__ == "__main__":
    main()
