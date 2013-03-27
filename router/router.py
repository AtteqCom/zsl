import importlib
from utils.string_helper import underscore_to_camelcase
from imp import reload
from utils.task_helper import TaskHelper

class Router:
    def __init__(self, app):
        self._mappings = {}
        # self._task_package = app.config['TASK_PACKAGE']

	self.set_task_package("sportky.tasks")
        self._app = app
        self._task_reloading = app.config['RELOAD']

    def get_task_package(self):
        return self._task_package

    def set_task_package(self, task_package):
        self._task_package = task_package

    def _load_module(self, module_name):
        return importlib.import_module(module_name)

    def is_task_reloading(self):
        return self._task_reloading

    def set_task_reloading(self, value):
        self._task_reloading = value

    '''
    Returns the task handling the given request path.
    '''
    def route(self, path):
        self._app.logger.debug("Routing path '%s'.", path)

        # Split the path into arrays - package names in the sportky.tasks package.
        path = path.split("/")
        module_name = "{0}.{1}".format(self.get_task_package(), ".".join(path))
        class_name = underscore_to_camelcase(path[-1])
        self._app.logger.debug("Module name '%s' and class name '%s'.", module_name, class_name)

        module = self._load_module(module_name)

        if self.is_task_reloading():
            reload(module)

        # Create the task using the injector initialization.
        cls = getattr(module, class_name)
        task = TaskHelper.instantiate(cls)

        self._app.logger.debug("Task object {0} created [{1}].".format(class_name, task))
        return (task, TaskHelper.get_callable(task))
