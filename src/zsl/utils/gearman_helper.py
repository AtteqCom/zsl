"""
:mod:`zsl.utils.import_helper`
------------------------------

.. moduleauthor:: Martin Babka
"""
import json
from typing import Any

from zsl import Config, inject
from zsl.gearman import gearman


@inject
def schedule_gearman_task(path: str, data: Any, config: Config) -> None:
    gm_client = gearman.GearmanClient(["{}:{}".format(config['GEARMAN']['host'], config['GEARMAN']['port'])])
    gm_client.submit_job(config['GEARMAN_TASK_NAME'], json.dumps(
        {'path': path, 'data': json.dumps(data)}), wait_until_complete=False, background=True)
