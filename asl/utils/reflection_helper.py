'''
:mod:`asl.utils.reflection_helper`

.. moduleauthor:: Martin Babka
'''
def extend(instance, new_class):
    instance.__class__ = type(
            '%s_extended_with_%s' % (instance.__class__.__name__, new_class.__name__),
            (new_class, instance.__class__, ),
            {}
        )

def add_mixin(base_class, mixin_class):
    base_class.__bases__ = (mixin_class, ) +  base_class.__bases__
    return base_class
