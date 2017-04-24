"""
:mod:`zsl.utils.deploy.apiary_doc_generator`
--------------------------------------------

Generates the API documentation suitable for the apiary.io. It parses all the files and finds the apiary.io definitions
in the documentary comments. Then outputs it to a file.

.. moduleauthor:: Martin Babka
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import os

import pydoc
import inspect
import pkgutil
import importlib
import logging

from zsl import inject
from zsl.router.method import get_method_packages
from zsl.router.task import TaskRouter


class ApiaryDoc(pydoc.Doc):

    _API_DOC_STR = "API Documentation:"

    def __init__(self):
        self._docs = []
        self._done = set()

    @staticmethod
    def _get_obj_id(obj):
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
        logging.debug('Adding {0}.'.format(obj_id))
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
        apistr = [x[m:] for x in apistr]

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
            logging.debug("Loading module {0} in {1}.".format(module_name, obj.__path__))
            try:
                module = loader.find_module(module_name).load_module(module_name)
                self.docmodule(module)
            except:
                pass

    def get_doc(self):
        return "FORMAT: 1A\n\n" + "\n\n".join(self._docs)


@inject(task_router=TaskRouter)
def generate_apiary_doc(task_router):
    """Generate apiary documentation.

    Create a Apiary generator and add application packages to it.

    :param task_router: task router, injected
    :type task_router: TaskRouter
    :return: apiary generator
    :rtype: ApiaryDoc
    """
    generator = ApiaryDoc()

    for m in task_router.get_task_packages() + get_method_packages():
        m = importlib.import_module(m)
        generator.docmodule(m)

    return generator
