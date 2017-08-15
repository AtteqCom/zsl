"""
:mod:`zsl.interface.gearman.task_filler`
----------------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function, unicode_literals

import json

import gearman

from zsl import Config, Injected, inject


@inject(config=Config)
def exec_task_filler(task_path, json_data, config=Injected):
    print("Initializing client.")
    gm_client = gearman.GearmanClient(["{0}:{1}".format(config['GEARMAN']['host'], config['GEARMAN']['port'])])
    print("Client initialized.")

    if json_data.startswith("file://"):
        with open(json_data[len("file://"):]) as f:
            json_data = f.read()

    ret_val = gm_client.submit_job(config['GEARMAN_TASK_NAME'], json.dumps(
        {'path': task_path, 'data': json.loads(json_data)}))

    print("Returned value '{0}'.".format(ret_val))
    output = json.loads(ret_val.result)['data']
    print("Returned data '{0}' of type '{1}'.".format(output, type(output)))
