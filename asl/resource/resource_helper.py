'''
Created on Sep 9, 2013

@author: Peter Morihladko
'''

from sqlalchemy.orm import class_mapper, joinedload

def filter_from_url_arg(model_cls, query, arg):
    '''
    Parse filter URL argument ``arg`` and apply to ``query``
    
    Example: 'column1<=value,column2==value' -> query.filter(Model.column1 <= value, Model.column2 == value)
    '''
    
    fields = arg.split(',')
    
    exprs = []
    for expr in fields:
        for operator, method in operator_to_method.items():
            if operator in expr:
                (column_name, value) = expr.split(operator)
                
                column_name = column_name.strip()
                value = value.strip()
                
                if hasattr(model_cls, column_name):
                    column = getattr(model_cls, column_name)
                    exprs.append(getattr(column, method)(value))
                else:
                    pass # TODO vyhod vynimku
          
        # TODO vyhod vynimku ak nenajde operator
    
    return query.filter(*exprs)

operator_to_method = {
    '==': '__eq__',
    '<=': '__le__',
    '<':  '__lt__',
    '>':  '__gt__',
    '>=': '__ge__',
    '!=': '__ne__'
}

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
    