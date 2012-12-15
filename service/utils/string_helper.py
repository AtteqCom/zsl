'''
Created on 15.12.2012

@author: Martin Babka
'''
def underscore_to_camelcase(value):
    def camelcase():
        while True:
            yield str.capitalize

    # TODO - better
    value = str(value)
    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))
