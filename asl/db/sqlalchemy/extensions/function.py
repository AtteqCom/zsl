'''
Created on 1.8.2013

@author: Martin Babka
'''
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import Numeric

def function(function_name):
    class function(expression.FunctionElement):
        type = Numeric()

    def function_impl(element, compiler, **kw):
        arg = list(element.clauses)
        return "%s(%s)" % (
            function_name,
            compiler.process(arg),
        )

    f = type('function_%s' % (function_name,), function.__bases__, dict(function.__dict__))
    f.name = function_name
    compiles(f)(function_impl)
    return f
