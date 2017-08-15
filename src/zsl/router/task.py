"""
:mod:`zsl.router.task`
------------------------
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta
from builtins import *
import importlib
import logging
from typing import Any, Callable, Dict, List, Tuple

from zsl import Config, inject
from zsl.errors import ZslError
from zsl.utils.string_helper import underscore_to_camelcase
from zsl.utils.task_helper import get_callable, instantiate

TASK_CONFIGURATION_NAME = 'TASKS'


class TaskNamespace(object):
    def __init__(self, namespace, task_configuration):
        # type: (str, TaskConfiguration)->None
        self._task_packages = []
        self._routes = {}
        self._task_configuration = task_configuration
        self._namespace = namespace

    def add_packages(self, packages):
        """
        Adds an automatic resolution of urls into tasks.
        :param packages: The url will determine package/module and the class.
        :return: self
        """
        # type: (List[str])->TaskNamespace
        assert isinstance(packages, list), "Packages must be list of strings."
        self._task_packages += packages
        return self

    def get_packages(self):
        # type:()->List[str]
        return list(self._task_packages)

    def add_routes(self, routes):
        """Adds the detailed mapping of urls to tasks.

        :param routes: Mapping which defines how urls of the namespace are
                       mapped to tasks. Each url (string) is mapped to a
                       callable which creates the task instance.

        :return: self
        """
        # type: (Dict[str, Callable])->TaskNamespace
        self._routes.update(routes)
        return self

    def get_routes(self):
        # type: ()->Dict[str, Callable]
        return self._routes.copy()

    def get_configuration(self):
        # type: ()->TaskConfiguration
        return self._task_configuration

    @property
    def namespace(self):
        # type:()->str
        return self._namespace


class TaskConfiguration(object):
    def __init__(self):
        self._namespaces = []  # type: List[TaskNamespace]

    def create_namespace(self, namespace):
        # type:(str)->TaskNamespace
        namespace = TaskNamespace(namespace, self)
        self._namespaces.append(namespace)
        return namespace

    @property
    def namespaces(self):
        return list(self._namespaces)


class RoutingError(ZslError):
    def __init__(self, path):
        msg = "Can not find task at path '{0}'.".format(path)
        super(RoutingError, self).__init__(msg)
        self._path = path

    @property
    def path(self):
        return self._path


class RouterStrategy(object):
    __metaclass__ = ABCMeta

    def can_route(self, path):
        # type:(str)->bool
        pass

    def route(self, path):
        # type:(str)->Callable
        pass


class PathTaskRouterStrategy(RouterStrategy):
    def __init__(self, task_configuration):
        # type: (TaskConfiguration)->None

        self._routes = {}
        for namespace_configuration in task_configuration.namespaces:
            namespace_routes = {}
            for k in namespace_configuration.get_routes():
                namespace_routes[namespace_configuration.namespace + '/' + k] = namespace_configuration.get_routes()[k]
            self._routes.update(namespace_routes)

    def can_route(self, path):
        return path in self._routes

    def route(self, path):
        return self._routes[path]


class PackageTaskRouterStrategy(RouterStrategy):
    def __init__(self, task_configuration, debug):
        # type: (TaskConfiguration)->None
        self._namespaces = task_configuration.namespaces
        self._debug = debug

    def can_route(self, path):
        return True

    def _load_module(self, module_name):
        # Debug loading provides better output.
        if self._debug:
            full = []
            for p in module_name.split('.'):
                full.append(p)
                importlib.import_module('.'.join(full))
        return importlib.import_module(module_name)

    def is_task_reloading(self):
        return self._debug

    def route(self, path):
        # type:(str)->Callable

        # Finding the path in task packages.
        logger = logging.getLogger(__name__)
        module_ = None
        exceptions = []
        class_name = None

        for task_namespace in self._namespaces:
            if not path.startswith(task_namespace.namespace):
                continue

            # Split the path into arrays - package names in the tasks package.
            class_name, package_path = self._split_path(path, task_namespace)
            task_packages = task_namespace.get_packages()
            module_, exceptions = self._find_task_in_namespace(task_packages, package_path, class_name)
            if module_ is not None:
                break

        if module_ is None:
            exception = RoutingError(path)
            logger.warning(str(exception))
            for e in exceptions:
                logger.error("Reason", exc_info=e)
            raise exception

        if self.is_task_reloading():
            importlib.reload(module_)
        cls = getattr(module_, class_name)
        return cls

    def _split_path(self, path, task_namespace):
        # type:(str, TaskNamespace)->Tuple[str, List[str]]
        package_path = path[len(task_namespace.namespace + '/'):]
        package_path = package_path.split("/")
        class_name = underscore_to_camelcase(package_path[-1])
        return class_name, package_path

    def _find_task_in_namespace(self, task_packages, package_path, class_name):
        logger = logging.getLogger(__name__)
        exceptions = []
        module_ = None
        for task_package in task_packages:
            module_name = "{0}.{1}".format(task_package, ".".join(package_path))

            try:
                logger.debug("Trying to load module with name '%s' and class name '%s'.",
                             module_name,
                             class_name)
                module_ = self._load_module(module_name)
                break
            except ImportError as e:
                exceptions.append(e)
                if self._debug:
                    logger.warning(
                        "Could not load module with name '%s' and class name '%s', '%s'; proceeding to next module.",
                        module_name, class_name, e)
        return module_, exceptions


class TaskRouter(object):
    @inject(config=Config, task_configuration=TaskConfiguration)
    def __init__(self, config, task_configuration):
        # type: (Config, TaskConfiguration) -> None
        self._config = config
        self._task_configuration = task_configuration  # type: TaskConfiguration
        self._strategies = [
            PathTaskRouterStrategy(self._task_configuration),
            PackageTaskRouterStrategy(self._task_configuration, self._config.get('DEBUG', False))
        ]

    def route(self, path):
        # type: (str)->Tuple[Any, Callable]
        """
        Returns the task handling the given request path.
        """
        logging.getLogger(__name__).debug("Routing path '%s'.", path)

        cls = None
        for strategy in self._strategies:
            if strategy.can_route(path):
                cls = strategy.route(path)
                break

        if cls is None:
            raise RoutingError(path)

        return self._create_result(cls)

    def _create_result(self, cls):
        # type:(Callable)->Tuple[Any, Callable]
        """
        Create the task using the injector initialization.
        :param cls:
        :return:
        """
        task = instantiate(cls)
        logging.getLogger(__name__).debug("Task object {0} created [{1}].".format(cls.__name__, task))
        return task, get_callable(task)
