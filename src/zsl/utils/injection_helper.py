"""
:mod:`zsl.utils.injection_helper`
---------------------------------

.. moduleauthor:: Martin Babka
"""
import functools
import inspect
import logging
from typing import Type

from injector import Binder, CallError, ClassProvider, Scope
from injector import inject as raw_inject
from injector import reraise

from zsl._state import get_current_app


def instantiate(cls):
    inj = get_current_app().injector

    if hasattr(cls, "__new__"):
        task = inj.create_object(cls)
    else:
        task = cls()

    return task


def inject(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # todo read_lock for injector
        return get_current_app().injector.call_with_injection(raw_inject(f), args=args, kwargs=kwargs)

    return wrapper


def simple_bind(binder: Binder, cls: Type, scope: Scope) -> None:
    binder.bind(interface=cls, to=ClassProvider(cls).get(binder.injector), scope=scope)
