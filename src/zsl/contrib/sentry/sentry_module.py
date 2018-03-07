"""
:mod:`zsl.contrib.modules.sentry_module`
-----------------------------------------

Sentry module is responsible for handling errors and sending them to a sentry
backend. Just provide a DSN (url) of the backend and you are all set up.

To add the Sentry support just add `SentryModule` to your container.

.. code-block:: python

    class MyApplicationContainer(WebContainer):
        sentry = SentryModule

Configuration
~~~~~~~~~~~~~

To configure one needs to provide a valid `SentryConfiguration` usually in
`default_settings.py` or in your profiles.

.. code-block:: python

    SENTRY = SentryConfiguration(dsn="...")

The following options are available:

    1. `dsn`: DSN/URl of your Sentry project,
    2. `environment`: the environment (release defaults to the version of your application),
    3. `tags`: additional tags str to str dictionary,
    4. `register_sentry_logging_handler`: bool value indicating if logging handler should be added to logging,
    5. `sentry_handler_logging_level`: minimal log level of log messages sent to sentry logging handler.

To test the functionality use CLI

.. code-block:: bash

    python app.py sentry test

"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *

from flask import logging
from injector import Binder, provides, singleton
from raven import Client, setup_logging
from raven.handlers.logging import SentryHandler
from raven.transport import ThreadedRequestsHTTPTransport

from zsl import Config, Module, Zsl, inject
from zsl.application.error_handler import register
from zsl.application.modules.cli_module import ZslCli
from zsl.contrib.sentry.sentry_config import SentryConfiguration
from zsl.errors import ErrorProcessor, ZslError
from zsl.utils.injection_helper import simple_bind

try:
    import raven
except ImportError:
    CommandLine = None
    logging.getLogger(__name__).exception(
        "Can not import sentry client raven. Please install it first `pip install zsl ["
        "sentry]`.")
    raise


class SentryCli(object):
    pass

    """Sentry CLI interface support."""

    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> None
        logging.getLogger(__name__).debug("Creating Sentry CLI.")

        @zsl_cli.cli.group()
        def sentry():
            pass

        @sentry.command(help='Send a test error to the Sentry backend.')
        def test():
            print('Sending test Sentry message.')
            raise ZslError("Sentry test error from Zsl.")

        self._sentry = sentry

    @property
    def sentry(self):
        return self._sentry


class SentryErrorProcessor(ErrorProcessor):

    @inject(config=SentryConfiguration, zsl=Zsl)
    def __init__(self, config, zsl):
        # type: (SentryConfiguration, Zsl)->None
        self._client = self._create_client(config, zsl)

        if config.register_logging_handler:
            self._register_logging_handler(config)

    @staticmethod
    def _create_client(config, zsl):
        # type: (SentryConfiguration, Zsl)->Client
        return Client(
            config.dsn,
            transport=ThreadedRequestsHTTPTransport,
            environment=config.environment,
            release=zsl.get_version(),
            tags=config.tags
        )

    def _register_logging_handler(self, config):
        # type: (SentryConfiguration)->SentryHandler
        handler = SentryHandler(self._client)
        handler.setLevel(config.sentry_handler_logging_level)
        setup_logging(handler)
        return handler

    def handle(self, e):
        logging.getLogger(__name__).info('Sending error message for {0}.'.format(e))
        self._client.captureException()


class SentryModule(Module):
    """Adds Sentry support."""

    SENTRY_CONFIG_NAME = 'SENTRY'

    @provides(SentryConfiguration)
    @inject(config=Config)
    def provide_sentry_configuration(self, config):
        # type: (Config) -> SentryConfiguration
        return config.get(SentryModule.SENTRY_CONFIG_NAME)

    def configure(self, binder):
        # type: (Binder) -> None
        simple_bind(binder, SentryCli, singleton)
        register(SentryErrorProcessor())
