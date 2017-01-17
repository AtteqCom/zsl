"""
:mod:`zsl.utils.reflection_helper`
----------------------------------

Helper module for OOP operations.

.. moduleauthor:: Martin Babka
"""
from __future__ import unicode_literals


def extend(instance, new_class):
    """

    :param instance:
    :param new_class:
    :return:
    """
    instance.__class__ = type(
        '%s_extended_with_%s' % (instance.__class__.__name__, new_class.__name__),
        (new_class, instance.__class__,),
        {}
    )


def add_mixin(base_class, mixin_class):
    base_class.__bases__ = (mixin_class,) + base_class.__bases__
    return base_class

