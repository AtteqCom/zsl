from injector import Binder
from injector import Module, provides, singleton

from zsl import Config
from zsl import inject
from zsl.application.error_handler import register
from zsl.errors import ErrorConfiguration, ERROR_CONFIG_NAME


class ErrorHandlerModule(Module):
    @provides(interface=ErrorConfiguration, scope=singleton)
    @inject(config=Config)
    def provide_error_config(self, config):
        # type: (Config)->ErrorConfiguration
        return config.get(ERROR_CONFIG_NAME, ErrorConfiguration())

    def configure(self, binder):
        @inject(error_config=ErrorConfiguration)
        def get_error_config(error_config):
            # type: (ErrorConfiguration)->ErrorConfiguration
            return error_config
            # type: (Binder)->None

        super(ErrorHandlerModule, self).configure(binder)
        for handler in get_error_config().handlers:
            register(handler)
