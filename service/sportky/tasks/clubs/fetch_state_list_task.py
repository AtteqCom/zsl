from injector import inject
from task.task_decorator import json_output
from sportky.service.state_service import StateService

class FetchStateListTask(object):

    @inject(state_service = StateService)
    def __init__(self, state_service):
        self._state_service = state_service

    @json_output
    def perform(self, data):
        states = []
        for s in self._state_service.fetch_list():
            states.append(s.get_app_model())

        return states
