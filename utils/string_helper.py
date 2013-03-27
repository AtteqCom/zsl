'''
Created on 15.12.2012

@author: Martin Babka
'''
import re
def underscore_to_camelcase(value):
    def camelcase():
        while True:
            yield str.capitalize

    value = str(value)
    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
