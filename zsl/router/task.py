"""
:mod:`zsl.router.task`
------------------------
"""
from __future__ import unicode_literals
from builtins import object

import importlib

from zsl import inject, Zsl, Config
from zsl.utils.string_helper import underscore_to_camelcase
from zsl.utils.task_helper import instantiate, get_callable


class TaskRouter(object):
    @inject(app=Zsl, config=Config)
    def __init__(self, app, config):
        # type: (Zsl, Config) -> None
        self._app = app
        self._config = config
        self._mappings = {}
        # Support for the settings with only one TASK_PACKAGE defined.
        self._task_packages = self._config.get('TASK_PACKAGES', (self._config.get('TASK_PACKAGE', 'zsl.tasks'),))
        self._debug = self._config['DEBUG']
        self._task_reloading = self._debug

    def get_task_packages(self):
        return self._task_packages

    def set_task_packages(self, task_packages):
        self._task_packages = task_packages

    def _load_module(self, module_name):
        # Debug loading provides better output.
        if self._debug:
            full = []
            for p in module_name.split('.'):
                full.append(p)
                importlib.import_module('.'.join(full))
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

        # Split the path into arrays - package names in the tasks package.
        path = path.split("/")
        class_name = underscore_to_camelcase(path[-1])

        # finding the path in task packages
        module_ = None
        exceptions = []
        for task_package in self.get_task_packages():
            module_name = "{0}.{1}".format(task_package, ".".join(path))

            try:
                self._app.logger.debug("Trying to load module with name '%s' and class name '%s'.", module_name,
                                       class_name)
                module_ = self._load_module(module_name)
                break
            except ImportError as e:
                exceptions.append(e)
                if self._debug:
                    self._app.logger.warn(
                        "Could not load module with name '%s' and class name '%s', '%s'; proceeding to next module.",
                        module_name, class_name, e)

        if module_ is None:
            msg = "Can not load task named {0} from {1}.".format(".".join(path), ",".join(self.get_task_packages()))
            self._app.logger.warn(msg)
            for e in exceptions:
                self._app.logger.error("Reason", exc_info=e)
            raise ImportError(msg)

        if self.is_task_reloading():
            importlib.reload(module_)

        # Create the task using the injector initialization.
        cls = getattr(module_, class_name)
        task = instantiate(cls)

        self._app.logger.debug("Task object {0} created [{1}].".format(class_name, task))
        return task, get_callable(task)
