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

from asl.application.service_application import service_application
app = service_application

if __name__ == "__main__":
    print "Initializing client."
    gm_client = gearman.GearmanClient(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])
    print "Client initialized."
    json_data = sys.argv[2]
    if json_data.startswith("file://"):
        with open(json_data[len("file://"):]) as f:
            json_data = f.read()
    ret_val = gm_client.submit_job(app.config['GEARMAN_TASK_NAME'], json.dumps({ 'path': sys.argv[1], 'data': json.loads(json_data) }))
    print "Returned value '{0}'.".format(ret_val)
    output = json.loads(ret_val.result)['data']
    print "Returned data '{0}' of type '{1}'.".format(output, type(output))
