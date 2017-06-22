"""
:mod:`zsl.application.initializers.web_initializer`
---------------------------------------------------
"""
from __future__ import unicode_literals

from zsl.interface.webservice.web_application_loader import load


class WebInitializer(object):
    """Initialize the web application."""
    @staticmethod
    def initialize():
        load()
