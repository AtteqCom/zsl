"""
:mod:`zsl.application.containers.web_container`
-----------------------------------------------
"""
from __future__ import unicode_literals

from zsl.application.containers.core_container import CoreContainer
from zsl.application.modules.web.web_context_module import WebContextModule


class WebContainer(CoreContainer):
    """Configuration for web application."""
    web_context = WebContextModule
