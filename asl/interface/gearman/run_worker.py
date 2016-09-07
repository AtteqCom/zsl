'''
:mod:`asl.interface.gearman.run_worker`

.. moduleauthor:: Martin Babka
'''

# Initialize app
import importer
importer.append_asl_path_to_pythonpath()
from asl.interface.importer import initialize_cli_application, InitializationContext
initialize_cli_application(InitializationContext(unit_test=False))

from asl.interface.gearman.worker import Worker
from asl.application.service_application import service_application as app

if __name__ == "__main__":
    print "Initializing Gearman worker."
    w = Worker(app)
    w.run()
