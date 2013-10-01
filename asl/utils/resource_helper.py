import importlib
from flask import request
from imp import reload

from asl.application.service_application import service_application
from asl.utils.string_helper import underscore_to_camelcase
from asl.utils.task_helper import instantiate

app = service_application

class MethodNotImplementedException(Exception):
    pass

def parse_resource_path(path):
    splits = path.split('/')
    
    return (splits[0], splits[1:])

def get_method(resource, method):
    if hasattr(resource, method) and callable(getattr(resource,method)):
        return getattr(resource,method)
    else:
        raise MethodNotImplementedException()

def get_resource_task(resource_path):
    class_name = underscore_to_camelcase(resource_path) + 'Resource'
    module_name = "{0}.{1}".format(app.config['RESOURCE_PACKAGE'], resource_path)

    try:
        module = importlib.import_module(module_name)
    except ImportError, e:
        app.logger.debug("Module %s resource does not exits", module_name)
        raise e

    # TODO if app.is_debug
    reload(module)

    # Create the resource using the injector initialization.
    try:
        cls = getattr(module, class_name)
    except AttributeError:
        raise ImportError("cannot find [{0}] in module [{1}]".format(class_name, module_name))
    resource = instantiate(cls)

    try:
        if request.method == 'POST':
            return get_method(resource, 'create')

        elif request.method == 'GET':
            return get_method(resource, 'read')

        elif request.method == 'PUT':
            return get_method(resource, 'update')

        elif request.method == 'DELETE':
            return get_method(resource, 'delete')

        else:
            app.logger.error("Invalid request method [%s] is requested for path [%s]", request.method, resource_path)

    except MethodNotImplementedException:
        app.logger.debug("MethodNotImplementedException raised for method [%s] and path [%s]", request.method, resource_path)
        return None
