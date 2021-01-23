"""
:mod:`zsl.application.initializers.unittest_initializer`
--------------------------------------------------------
"""
from zsl import ApplicationContext, Config, inject


class UnitTestInitializer(object):
    # TODO: Change to iface

    """Initializer handling the unit test settings."""
    @staticmethod
    @inject
    def initialize(config: Config) -> None:

        if not UnitTestInitializer.is_unit_testing():
            return

        if 'TEST_DATABASE_URI' in config:
            config['DATABASE_URI'] = config['TEST_DATABASE_URI']

        if 'TEST_DATABASE_ENGINE_PROPS' in config:
            config['DATABASE_ENGINE_PROPS'] = config[
                'TEST_DATABASE_ENGINE_PROPS']

    @staticmethod
    @inject
    def is_unit_testing(ctx: ApplicationContext) -> bool:
        return ctx.unit_testing
