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
    splits = path.split('/', 1)
    splits_num = len(splits)

    resource = None
    param = None

    if splits_num > 0:
        resource = splits[0]

    if splits_num > 1:
        param = splits[1]

    return (resource, param)

def get_method(resource, method):
    if hasattr(resource, method) and callable(getattr(resource,method)):
        return getattr(resource,method)
    else:
        raise MethodNotImplementedException()

def get_resource_task(resource_path):
    class_name = underscore_to_camelcase(resource_path)
    module_name = app.config['RESOURCE_PACKAGE'] + resource_path

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        app.logger.debug("Module %s resource does not exits", module_name)
        return None

    # TODO if app.is_debug
    reload(module)

    # Create the resource using the injector initialization.
    cls = getattr(module, class_name)
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
