'''
Created on 1.8.2013

@author: Martin Babka
'''
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

def function(function_name, data_type):
    class function(expression.FunctionElement):
        pass

    def function_impl(element, compiler, **kw):
        args = ", ".join(map(lambda x: compiler.process(x), list(element.clauses)))
        return "%s(%s)" % (
            function_name,
            args
        )

    f = type('function_%s' % (function_name,), function.__bases__, dict(function.__dict__))
    f.name = function_name
    f.type = data_type
    compiles(f)(function_impl)
    return f
