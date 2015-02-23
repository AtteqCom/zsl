'''
Generates the API documentation suitable for the apiari.io. It parses all the files and finds the apiari definitions
in the documentary comments. Then outputs it to a file.

Created on 21.11.2014

@author: Martin Babka
'''

import pydoc
import inspect
import pkgutil
from asl.application import service_application
from asl.router.method import get_method_packages
import sys
import os
service_application.initialize_dependencies()
from asl.router.task import TaskRouter
import importlib

class ApiariDoc(object, pydoc.Doc):

    _API_DOC_STR = "API Documentation:"

    def __init__(self):
        self._docs = []
        self._done = set()

    def _get_obj_id(self, obj):
        if hasattr(obj, '__path__'):
            return obj.__path__[0]
        if hasattr(obj, '__file__'):
            return obj.__file__
        if hasattr(obj, '__name__'):
            return obj.__name__
        else:
            return obj

    def _add_doc(self, obj):
        obj_id = self._get_obj_id(obj)
        if obj_id in self._done:
            return
        service_application.logger.debug('Adding {0}.'.format(obj_id))
        self._done.add(obj_id)

        apistr = ""
        try:
            if obj.__doc__ is None:
                return

            start = obj.__doc__.find(self._API_DOC_STR)
            if start == -1:
                return
            apistr = obj.__doc__[start + len(self._API_DOC_STR):]
        except:
            return

        apistr = apistr.splitlines()
        while apistr[0].isspace() or apistr[0] == "":
            apistr = apistr[1:]

        def white_space_at_beginning(l):
            c = 0
            i = 0
            length = len(l)
            while i < length:
                if l[i].isspace():
                    c += 1
                else:
                    return c
                i += 1
            return c

        m = white_space_at_beginning(apistr[0])
        for l in apistr:
            if l.isspace() or l == "":
                continue
            wl = white_space_at_beginning(l)
            if m > wl:
                m = wl
        apistr = map(lambda x : x[m:], apistr)

        self._docs.append("\n".join(apistr))

    def docmodule(self, obj, name=None, *args):
        if self._get_obj_id(obj) in self._done:
            return

        self._add_doc(obj)
        for _key, value in inspect.getmembers(obj, inspect.isclass):
            self._add_doc(value)
        for _key, value in inspect.getmembers(obj, lambda x: hasattr(x, '__call__')):
            self._add_doc(value)

        for _key, value in inspect.getmembers(obj, inspect.ismodule):
            self.docmodule(value)

        if not hasattr(obj, '__path__'):
            return
        if obj.__path__[0].startswith(os.path.dirname(sys.executable)):
            return

        for loader, module_name, _ispkg in pkgutil.iter_modules(obj.__path__):
            service_application.logger.debug("Loading module {0} in {1}.".format(module_name, obj.__path__))
            try:
                module = loader.find_module(module_name).load_module(module_name)
                self.docmodule(module)
            except:
                pass

    def get_doc(self):
        return "FORMAT: 1A\n\n" + "\n\n".join(self._docs)

if __name__ == "__main__":
    d = ApiariDoc()
    for m in TaskRouter(service_application).get_task_packages() + get_method_packages():
        m = importlib.import_module(m)
        d.docmodule(m)
    print d.get_doc()
