'''
Created on 15.12.2012

@author: Martin Babka
'''

# Append the right path to the PYTHONPATH for the CGI script to work.
import os
import sys
sys.path.append(os.path.abspath('../../'))

from application.service_application import service_application
from interface.gearman.worker import Worker

app = service_application

if __name__ == "__main__":
    print "Initializing Gearman worker."
    w = Worker(app)
    w.run()
