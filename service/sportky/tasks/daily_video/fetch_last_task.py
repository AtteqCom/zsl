from task.task_decorator import json_output
from injector import inject
import logging

class FetchLastTask(object):

    @json_output
    def perform(self, data):
        return	[
                {'id': 1, 'name': 'Video 1', 'image': '/img/dummy-club.png', 'url': 'http://www.atteq.com'},
                {'id': 2, 'name': 'Video 2', 'image': '/img/dummy-club.png', 'url': 'http://www.atteq.com'},
                {'id': 3, 'name': 'Video 3', 'image': '/img/dummy-club.png', 'url': 'http://www.atteq.com'},
                {'id': 4, 'name': 'Video 4', 'image': '/img/dummy-club.png', 'url': 'http://www.atteq.com'},
                {'id': 5, 'name': 'Video 5', 'image': '/img/dummy-club.png', 'url': 'http://www.atteq.com'},
        ]
