'''
Created on 15.12.2012

@author: Martin Babka
'''

from asl.interface import importer
importer.append_pythonpath()

from asl.application.service_application import service_application
from asl.interface.gearman.worker import Worker

app = service_application

if __name__ == "__main__":
    print "Initializing Gearman worker."
    w = Worker(app)
    w.run()
