"""
:mod:`zsl.utils.resource_helper`
--------------------------------

Helper module for resource management.
"""
# TODO describe what model resource is and use cases

from __future__ import unicode_literals
import importlib
import logging
from typing import Callable, Union, List, Dict
from flask import request

from zsl.utils.string_helper import underscore_to_camelcase
from zsl.utils.task_helper import instantiate
from zsl.resource.model_resource import ModelResource
from zsl.interface.resource import ResourceResult

from zsl import inject, Config, Injected, Zsl


class MethodNotImplementedException(Exception):
    """Exception raised on missing method"""
    pass


def parse_resource_path(path):
    """Split the path to its elements.

    :param path: URL path
    :type path: str
    :return: name and rest of the path
    :rtype: tuple(str, list(str))
    """
    splits = path.split('/')

    return splits[0], splits[1:]


def get_method(resource, method):
    """Test and return a method by name on resource.

    :param resource: resource object
    :type resource: object
    :param method: method name
    :type method: str
    :return: bounded method
    :raises MethodNotImplementedException: when method not found
    """
    if hasattr(resource, method) and callable(getattr(resource, method)):
        return getattr(resource, method)
    else:
        raise MethodNotImplementedException()


@inject(config=Config)
def get_resource_task(resource_path, config=Injected):
    # type: (str, Config) -> Callable[[str, Dict, Dict], Union[List[AppModel], AppModel, ResourceResult]]
    """Search and return a bounded method for given path.

    :param resource_path: resource path
    :type resource_path: str
    :param config: current configuration, injected
    :type config: Config
    :return: bounded method or None when not found
    :raises NameError: when can't find given resource by path
    """
    class_name = underscore_to_camelcase(resource_path) + 'Resource'

    resource_packages = config['RESOURCE_PACKAGES'] if 'RESOURCE_PACKAGES' in config else (config['RESOURCE_PACKAGE'],)

    resource = None
    for resource_package in resource_packages:
        module_name = "{0}.{1}".format(resource_package, resource_path)

        try:
            module = importlib.import_module(module_name)

            try:
                cls = getattr(module, class_name)

                resource = instantiate(cls)
                break
            except AttributeError:
                raise NameError("Can't find resource [{0}]".format(resource_path))

        except ImportError:

            # try to find __exposer__
            try:
                exposer = importlib.import_module(resource_package + '.__exposer__')

                resource = exposer.get_resource(class_name)
                break
            except Exception as e:
                logging.error("Can not load resource {0} [{1}].".format(resource_path, e))
                pass

    if resource is None:
        raise NameError("Can't find resource [{0}]".format(resource_path))

    try:
        if request.method == 'POST':
            return get_method(resource, 'create')

        elif request.method == 'GET':
            return get_method(resource, 'read')

        elif request.method == 'PUT' or request.method == 'PATCH':
            return get_method(resource, 'update')

        elif request.method == 'DELETE':
            return get_method(resource, 'delete')

        else:
            logging.error("Invalid request method [%s] is requested for path [%s]", request.method, resource_path)

    except MethodNotImplementedException:
        logging.error(
            "MethodNotImplementedException raised for method [%s] and path [%s]",
            request.method,
            resource_path
        )
        return None


@inject(app=Zsl)
def create_model_resource(resource_map, name, app=Injected):
    """Create a model resource from a dict ``resource_map``
    {'resource name': ('model package', 'model class')}

    :param resource_map: dict with resource descriptions
    :type resource_map: dict(str, tuple(str))
    :param name: name of the concrete resource
    :param app: current application, injected
    :type app: Zsl
    :return: instantiated model resource
    """
    try:
        resource_description = resource_map[name]
        if len(resource_description) == 2:
            module_name, model_name = resource_map[name]
            resource_class = ModelResource
        elif len(resource_description) == 3:
            module_name, model_name, resource_class = resource_map[name]
        else:
            raise ImportError("Invalid resource description for resource '{0}'".format(name))
    except KeyError:
        raise ImportError("Missing resource description for resource '{0}'".format(name))

    module = importlib.import_module(module_name)
    model_cls = getattr(module, model_name)

    return app.injector.create_object(resource_class, {'model_cls': model_cls})
