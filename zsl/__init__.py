"""
:mod:`zsl` -- zsl module
========================

Main service module.

   :platform: Unix, Windows
   :synopsis: The Atteq Service Layer. Service for exposing data to clients. Just provides DB access, feeds access and \
    other various aspects of service applications.

.. moduleauthor:: Martin Babka <babka@atteq.com>
"""
from __future__ import unicode_literals

__version__ = '0.15.7'

from flask import Config

from injector import Module

from zsl.application.initialization_context import InitializationContext as ApplicationContext

from zsl.utils.injection_helper import inject
from zsl.application.service_application import ServiceApplication

Zsl = ServiceApplication

# placeholder for default value used in function declaration for arguments which will be injected
Injected = None
