import importlib
from flask import request

from asl.application.service_application import service_application as app
from asl.utils.string_helper import underscore_to_camelcase
from asl.utils.task_helper import instantiate
from asl.resource.model_resource import ModelResource

resource_packages = app.config['RESOURCE_PACKAGES'] if 'RESOURCE_PACKAGES' in app.config else (app.config['RESOURCE_PACKAGE'],)

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
            except ImportError:
                pass
            
    if resource is None:
        raise NameError("Can't find resource [{0}]".format(resource_path))

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
    
def create_model_resource(resource_map, name):
    '''
    Create a model resource from a dict ``resource_map`` {'resource name': ('model package', 'model class')}
    '''
    try:
        module_name, model_name = resource_map[name]
    except KeyError:
        raise ImportError()

    module = importlib.import_module(module_name)
    model_cls = getattr(module, model_name)
    
    return app.get_injector().create_object(ModelResource, {'model_cls': model_cls})    

