'''
:mod:`asl.resource.resource_helper`

.. moduleauthor:: Peter Morihladko
'''

from sqlalchemy.orm import class_mapper, joinedload
from sqlalchemy import desc, asc

def filter_from_url_arg(model_cls, query, arg):
    '''
    Parse filter URL argument ``arg`` and apply to ``query``

    Example: 'column1<=value,column2==value' -> query.filter(Model.column1 <= value, Model.column2 == value)
    '''

    fields = arg.split(',')
    mapper = class_mapper(model_cls)

    exprs = []
    joins = []
    for expr in fields:
        if expr == "":
            continue

        e_mapper = mapper
        e_model_cls = model_cls

        operator = None
        method = None
        for op, m in operator_to_method.items():
            if op in expr:
                operator = op
                method = m

        if operator is None:
            raise Exception('No operator in expression "{0}".'.format(expr))

        (column_names, value) = expr.split(operator)

        column_names = column_names.split('__')
        value = value.strip()

        for column_name in column_names:
            if column_name in e_mapper.relationships:
                joins.append(column_name)
                e_model_cls = e_mapper.attrs[column_name].mapper.class_
                e_mapper = class_mapper(e_model_cls)

        if hasattr(e_model_cls, column_name):
            column = getattr(e_model_cls, column_name)
            exprs.append(getattr(column, method)(value))
        else:
            raise Exception('Invalid property {0} in class {1}.'.format(column_name, e_model_cls))


    return query.join(*joins).filter(*exprs)

operator_to_method = {
    '::like::': 'like',
    '==': '__eq__',
    '<=': '__le__',
    '>=': '__ge__',
    '!=': '__ne__',
    '<':  '__lt__',
    '>':  '__gt__'
}

def order_from_url_arg(model_cls, query, arg):
    fields = arg.split(',')
    mapper = class_mapper(model_cls)
    
    orderings = []
    joins = []
    for field in fields:
        e_mapper = mapper
        e_model_cls = model_cls
        
        if field[0] == '-':
            column_names = field[1:]
            direction = 'desc'
        else:
            column_names = field
            direction = 'asc'
            
        column_names = column_names.split('__')
        
        for column_name in column_names:
            if column_name in e_mapper.relationships:
                joins.append(column_name)
                e_model_cls = e_mapper.attrs[column_name].mapper.class_
                e_mapper = class_mapper(e_model_cls)

        if hasattr(e_model_cls, column_name):
            column = getattr(e_model_cls, column_name)
            order_by = asc(column) if direction == 'asc' else desc(column)
            orderings.append(order_by)
        else:
            raise Exception('Invalid property {0} in class {1}.'.format(column_name, model_cls))

    return query.join(*joins).order_by(*orderings)

def create_related_tree(fields):
    tree = {}
    for field in fields:
        fs = field.split('__')
        node = tree

        for f in fs:
            if f not in node:
                node[f] = {}
            node = node[f]

    # replace empty {} with None, to represent leafs
    q = [tree]
    while len(q) > 0:
        node = q.pop()

        for k,v in node.items():
            if len(v) > 0:
                q.append(v)
            else:
                node[k] = None

    return tree

def apply_related(model_cls, query, related_fields):
    """

    """
    mapper = class_mapper(model_cls)

    loads = []

    # TODO zatial iba pre
    for field in related_fields:
        if field in mapper.relationships:
            loads.append(joinedload(getattr(model_cls, field)))

    if loads:
        query = query.options(*loads)

    return query

def related_from_fields(fields):
    return [field.rsplit('__', 1)[0] for field in fields if '__' in field]
