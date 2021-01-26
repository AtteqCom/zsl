"""
:mod:`zsl.interface.gearman.task_filler`
----------------------------------------

.. moduleauthor:: Martin Babka
"""

import json

from zsl import Config, inject
from zsl.gearman import gearman


@inject
def exec_task_filler(task_path: str, json_data: str, config: Config) -> None:
    print("Initializing client.")
    gm_client = gearman.GearmanClient(["{}:{}".format(config['GEARMAN']['host'], config['GEARMAN']['port'])])
    print("Client initialized.")

    if json_data.startswith("file://"):
        with open(json_data[len("file://"):]) as f:
            json_data = f.read()

    ret_val = gm_client.submit_job(config['GEARMAN_TASK_NAME'], json.dumps(
        {'path': task_path, 'data': json.loads(json_data)}))

    print("Returned value '{}'.".format(ret_val))
    output = json.loads(ret_val.result)['data']
    print("Returned data '{}' of type '{}'.".format(output, type(output)))
