from task.task_decorator import json_input, json_output

class SimpleTask(object):
    @json_input
    @json_output
    def perform(self, data):
        return ["Simple task with data '{0}' of type {1}.".format(data.get_data(), type(data.get_data()))]
