"""
:mod:`zsl.utils.import_helper`
------------------------------

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals

import json

import gearman

from zsl import Config, inject


@inject(config=Config)
def schedule_gearman_task(path, data, config):
    gm_client = gearman.GearmanClient(["{0}:{1}".format(config['GEARMAN']['host'], config['GEARMAN']['port'])])
    gm_client.submit_job(config['GEARMAN_TASK_NAME'], json.dumps(
        {'path': path, 'data': json.dumps(data)}), wait_until_complete=False, background=True)
