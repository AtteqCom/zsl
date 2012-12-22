'''
Created on 20.12.2012

@author: Martin Babka
'''
import gearman

# Append the right path to the PYTHONPATH for the CGI script to work.
import os
import sys
import json
sys.path.append(os.path.abspath('../../'))

from application.service_application import service_application
app = service_application

if __name__ == "__main__":
    print "Initializing client."
    gm_client = gearman.GearmanClient(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
    print "Client initialized."
    ret_val = gm_client.submit_job("task", json.dumps({ 'path': sys.argv[1], 'data': json.loads(sys.argv[2]) }))
    print "Returned value '{0}'.".format(ret_val)
    output = json.loads(ret_val.result)['data']
    print "Returned data '{0}' of type '{1}'.".format(output, type(output))
