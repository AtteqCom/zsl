"""
:mod:`zsl.interface.gearman.run_worker`

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function
from __future__ import unicode_literals

# Initialize app
from zsl.interface.gearman import importer
importer.append_asl_path_to_pythonpath()
from zsl.interface.importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

from zsl.interface.gearman.worker import Worker
from zsl.application.service_application import service_application as app

if __name__ == "__main__":
    print("Initializing Gearman worker.")
    w = Worker(app)
    w.run()
