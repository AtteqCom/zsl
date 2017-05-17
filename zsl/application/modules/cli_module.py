import logging

from injector import Module, singleton, Binder

from zsl.interface.run import cli


class ZslCli:
    def __init__(self):
        logging.getLogger(__name__).debug("Creating ZSL CLI.")
        self._cli = cli

    @property
    def cli(self):
        return self._cli

    def __call__(self, *args, **kwargs):
        cli()


class CliModule(Module):
    """Adds Alembic support for migrations."""

    def configure(self, binder):
        # type: (Binder) -> None
        zsl_cli = ZslCli()
        binder.bind(
            ZslCli,
            to=zsl_cli,
            scope=singleton
        )
