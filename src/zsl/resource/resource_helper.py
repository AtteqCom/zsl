"""
:mod:`zsl.resource.resource_helper`
-----------------------------------

.. moduleauthor:: Peter Morihladko
"""
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import class_mapper, joinedload


def filter_from_url_arg(model_cls, query, arg, query_operator=and_,
                        arg_types=None):
    """
    Parse filter URL argument ``arg`` and apply to ``query``

    Example: 'column1<=value,column2==value' -> query.filter(Model.column1 <= value, Model.column2 == value)
    """

    fields = arg.split(',')
    mapper = class_mapper(model_cls)

    if not arg_types:
        arg_types = {}

    exprs = []
    joins = set()
    for expr in fields:
        if expr == "":
            continue

        e_mapper = mapper
        e_model_cls = model_cls

        operator = None
        method = None
        for op in operator_order:
            if op in expr:
                operator = op
                method = operator_to_method[op]
                break

        if operator is None:
            raise Exception('No operator in expression "{0}".'.format(expr))

        (column_names, value) = expr.split(operator)

        column_names = column_names.split('__')
        value = value.strip()

        for column_name in column_names:
            if column_name in arg_types:
                typed_value = arg_types[column_name](value)
            else:
                typed_value = value

            if column_name in e_mapper.relationships:
                joins.add(column_name)
                e_model_cls = e_mapper.attrs[column_name].mapper.class_
                e_mapper = class_mapper(e_model_cls)

        if hasattr(e_model_cls, column_name):
            column = getattr(e_model_cls, column_name)
            exprs.append(getattr(column, method)(typed_value))
        else:
            raise Exception('Invalid property {0} in class {1}.'.format(column_name, e_model_cls))

    exprs = _join_equal_columns_to_or(exprs)

    if joins:
        query = query.join(*joins)

    return query.filter(query_operator(*exprs))


def _join_equal_columns_to_or(filter_expressions):
    # compatibility magic, in 2.0 get_children() will return itertools.chain which is not subscriptable
    # so next(iter(chain)) will return the first element not only for chain but also for list
    #
    # 2.0 has a better access with .left/.right attributes, fix when we drop 1.3 support
    columns = list(next(iter(fe.get_children())) for fe in filter_expressions)
    if len(columns) == len(set(columns)):
        return filter_expressions

    joined_expressions = {}
    for filter_expression in filter_expressions:
        column = next(iter(filter_expression.get_children()))
        if column in joined_expressions:
            joined_expressions[column].append(filter_expression)
        else:
            joined_expressions[column] = [filter_expression]

    final_expressions = []
    for _, expressions in joined_expressions.items():
        if len(expressions) == 0:
            continue
        elif len(expressions) == 1:
            final_expressions.append(expressions[0])
        else:
            final_expressions.append(or_(*expressions))

    return final_expressions


operator_to_method = {
    '::like::': 'like',
    '==': '__eq__',
    '<=': '__le__',
    '>=': '__ge__',
    '!=': '__ne__',
    '<': '__lt__',
    '>': '__gt__'
}
operator_order = ['::like::', '==', '<=', '>=', '!=', '<', '>']


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

    if joins:
        query = query.join(*joins)

    return query.order_by(*orderings)


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

        for k, v in node.items():
            if len(v) > 0:
                q.append(v)
            else:
                node[k] = None

    return tree


def model_tree(name, model_cls, visited=None):
    """Create a simple tree of model's properties and its related models.

    It traverse trough relations, but ignore any loops.

    :param name: name of the model
    :type name: str
    :param model_cls: model class
    :param visited: set of visited models
    :type visited: list or None
    :return: a dictionary where values are lists of string or other \
    dictionaries
    """
    if not visited:
        visited = set()

    visited.add(model_cls)

    mapper = class_mapper(model_cls)
    columns = [column.key for column in mapper.column_attrs]
    related = [model_tree(rel.key, rel.mapper.entity, visited)
               for rel in mapper.relationships if rel.mapper.entity not in visited]

    return {name: columns + related}


def flat_model(tree):
    """Flatten the tree into a list of properties adding parents as prefixes."""
    names = []
    for columns in tree.values():
        for col in columns:
            if isinstance(col, dict):
                col_name = list(col)[0]
                names += [col_name + '__' + c for c in flat_model(col)]
            else:
                names.append(col)

    return names


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
