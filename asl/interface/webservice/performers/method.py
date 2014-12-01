'''
Created on 25.11.2014

@author: Martin Babka
'''
from asl.router.method import get_method_packages
import importlib

for package in get_method_packages():
    module = importlib.import_module(package)
    if hasattr(module, '__exposer__'):
        getattr(module, '__exposer__')()
