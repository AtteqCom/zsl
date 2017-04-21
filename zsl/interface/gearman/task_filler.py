"""
:mod:`zsl.interface.gearman.task_filler`
----------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function
from __future__ import unicode_literals


import sys
import gearman
import json

from zsl import Zsl

if __name__ == "__main__":

    app = Zsl(__name__)

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: task_filler.py <task name> <task data (file:// for file input, otherwise raw data)>\n")
        exit(1)

    print("Initializing client.")
    gm_client = gearman.GearmanClient(["{0}:{1}".format(app.config['GEARMAN']['host'], app.config['GEARMAN']['port'])])

    print("Client initialized.")
    json_data = sys.argv[2]
    if json_data.startswith("file://"):
        with open(json_data[len("file://"):]) as f:
            json_data = f.read()
    ret_val = gm_client.submit_job(app.config['GEARMAN_TASK_NAME'], json.dumps(
        {'path': sys.argv[1], 'data': json.loads(json_data)}))
    print("Returned value '{0}'.".format(ret_val))
    output = json.loads(ret_val.result)['data']
    print("Returned data '{0}' of type '{1}'.".format(output, type(output)))
