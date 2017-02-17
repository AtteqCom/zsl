"""
:mod:`zsl.interface.gearman.run_worker`
---------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function
from __future__ import unicode_literals

# Initialize app
from zsl.interface.importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

from zsl.interface.gearman.worker import GearmanTaskQueueWorker


def main():
    print("Initializing Gearman worker.")
    w = GearmanTaskQueueWorker()
    w.run()

if __name__ == "__main__":
    main()
