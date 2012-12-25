import importlib
from utils.string_helper import underscore_to_camelcase

class Router:
    def __init__(self, app):
        self.__mappings = {}
        # self.__task_package = app.config['TASK_PACKAGE']

	self.set_task_package("sportky.tasks")
        self.__app = app

    def get_task_package(self):
        return self.__task_package

    def set_task_package(self, task_package):
        self.__task_package = task_package

    def __load_module(self, module_name):
        return importlib.import_module(module_name)

    '''
    Returns the task handling the given request path.
    '''
    def route(self, path):
        self.__app.logger.debug("Routing path '%s'.", path)

        # Split the path into arrays - package names in the sportky.tasks package.
        path = path.split("/")
        module_name = "{0}.{1}".format(self.get_task_package(), ".".join(path))
        class_name = underscore_to_camelcase(path[-1])
        self.__app.logger.debug("Module name '%s' and class name '%s'.", module_name, class_name)

        module = self.__load_module(module_name)
        injector = self.__app.get_injector()

        # Create the task using the injector initialization.
        task = injector.create_object(getattr(module, class_name))

        self.__app.logger.debug("Task object {0} created [{1}].".format(class_name, task))
        task_callable = getattr(task, "perform")
        return (task, task_callable)
