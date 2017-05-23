"""
:mod:`zsl.interface.webservice.web_application_loader`
------------------------------------------------------
"""

from __future__ import unicode_literals
# Now import the application and the remaining stuff.

from zsl.interface.webservice.performers.default import create_not_found_mapping
from zsl.interface.webservice.performers.resource import create_resource_mapping
from zsl.interface.webservice.performers.task import create_web_task
from zsl.interface.webservice.performers.method import call_exposers_in_method_packages


def load():
    _load_performers()


def _load_performers():
    """
    Import in this form is necessary so that we avoid the unwanted behavior and immediate initialization of the
    application objects. This makes the initialization procedure run in the time when it is necessary and has every
    required resources.
    """
    create_not_found_mapping()
    create_resource_mapping()
    create_web_task()
    call_exposers_in_method_packages()
