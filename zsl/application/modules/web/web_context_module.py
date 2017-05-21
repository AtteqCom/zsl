import logging

import click
from injector import provides, singleton

from zsl import Zsl, inject
from zsl.application.initialization_context import InitializationContext
from zsl.application.initializers.web_initializer import WebInitializer
from zsl.application.modules.cli_module import ZslCli
from zsl.application.modules.context_module import DefaultContextModule, default_initializers
from zsl.utils.injection_helper import simple_bind

#: Initializers used in unit web applications
web_initializers = default_initializers + (WebInitializer,)


class WebCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> WebCli

        @zsl_cli.cli.group(help='Web related tasks.')
        def web():
            pass

        @web.command(help="Run web server and serve the application")
        @click.option('--host', '-h', help="host to bind to", default='127.0.0.1')
        @click.option('--port', '-p', help="port to bind to", default=5000)
        @inject(app=Zsl)
        def start(app, host, port):
            app.run_web(host=host, port=port)

        self._web = web

    @property
    def web(self):
        return self._web


class WebContextModule(DefaultContextModule):
    """Adds web application context to current configuration."""

    def _create_context(self):
        logging.getLogger(__name__).debug("Creating web context.")
        return InitializationContext(initializers=web_initializers)

    @provides(interface=WebCli, scope=singleton)
    def provide_web_cli(self):
        return WebCli()

    def configure(self, binder):
        super(WebContextModule, self).configure(binder)
        # type: (Binder) -> None
        simple_bind(binder, WebCli, singleton)
