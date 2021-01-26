from injector import Binder, Module, inject, provider

from zsl import Config
from zsl.application.error_handler import register
from zsl.errors import ERROR_CONFIG_NAME, ErrorConfiguration


class ErrorHandlerModule(Module):

    @provider
    @inject
    def provide_error_config(self, config: Config) -> ErrorConfiguration:
        # type: (Config)->ErrorConfiguration
        return config.get(ERROR_CONFIG_NAME, ErrorConfiguration())

    def configure(self, binder: Binder) -> None:
        error_config = binder.injector.get(ErrorConfiguration)
        super().configure(binder)
        for handler in error_config.handlers:
            register(handler)
