'''
Created on 15.12.2012

.. moduleauthor:: Martin Babka
'''

# Initialize app
import importer
importer.append_asl_path_to_pythonpath()
from asl.interface.importer import initialize_cli_application
initialize_cli_application()

from asl.interface.gearman.worker import Worker
from asl.application.service_application import service_application as app

if __name__ == "__main__":
    print "Initializing Gearman worker."
    w = Worker(app)
    w.run()
