"""
:mod:`zsl.contrib.alembic.alembic_module`
-----------------------------------------

Alembic module is responsible for handling database migrations for SqlAlchemy
database backend. The complete documentation of the Alembic project,
all the options and command may be found `Alembic website
<http://alembic.zzzcomputing.com/en/latest/index.html>`_.

If you need database migrations just install `alembic` extra of `zsl`
package. Then you may use `alembic` commands from ZSL cli interface via
`alembic` command.

Just use a standard way of calling cli with a container having `AlembicModule`.

.. code-block:: python

    class MyApplicationContainer(WebContainer):
        alembic = AlembicModule


    @inject(zsl_cli=ZslCli)
    def main(zsl_cli: ZslCli) -> None:
        zsl_cli()


    if __name__ == "__main__":
        os.environ[SETTINGS_ENV_VAR_NAME] = ... or set_profile('my-profile')
        app = Zsl(__name__, modules=MyApplicationContainer.modules())
        main()

Configuration
~~~~~~~~~~~~~

To configure one needs to provide a valid `AlembicConfiguration` usually in
`default_settings.py`

.. code-block:: python

    ALEMBIC = AlembicConfiguration(alembic_directory="...")

Then all the required files will be stored in the directory. Also the
`alembic.ini` file will be stored there although this is not a standard way.

When using `AlembicCli` interface the alembic commands will be functional
though.

A little setup is required so that the connection is opened correctly. In
`alembic.ini` in the given directory remove the following line.

.. code-block:: ini

    sqlalchemy.url = driver://user:pass@localhost/dbname

Also set `script_location` to `.` so that it does not rely on absolute paths

.. code-block:: ini

    script_location = .

Then in `env.py`, since we removed the `sqlalchemy.url` we need to use a ZSL
engine created using the correct urls from settings. To do so define the
routines `run_migrations_offline` and `run_migrations_online` so that they
use a correct `Engine`.

.. code-block:: python

    @inject(zsl_config=Config)
    def run_migrations_offline(zsl_config):
        url = zsl_config['DATABASE_URI']
        context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

        with context.begin_transaction():
            context.run_migrations()


    @inject(engine=Engine)
    def run_migrations_online(engine):
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()


"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *  # NOQA
import logging
import os

import click
from click.core import Context
from injector import Binder, Module, provides, singleton

from zsl import Config, inject
from zsl.application.modules.cli_module import ZslCli
from zsl.contrib.alembic.alembic_config import AlembicConfiguration
from zsl.utils.injection_helper import simple_bind

try:
    from alembic.config import CommandLine
except ImportError:
    CommandLine = None
    logging.getLogger(__name__).exception(
        "Can not import alembic. Please install it first `pip install zsl ["
        "alembic]`.")
    raise


class AlembicCli(object):
    """Alembic Cli interface support."""

    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> AlembicCli
        logging.getLogger(__name__).debug("Creating Alembic CLI.")

        @zsl_cli.cli.command(help='Run alembic maintenance tasks.',
                             context_settings=dict(
                                 ignore_unknown_options=True,
                                 allow_extra_args=True
                             ))
        @click.pass_context
        def alembic(ctx):
            # type: (Context) -> None
            self.call_alembic(ctx.args)

        self._alembic = alembic

    @property
    def alembic(self):
        return self._alembic

    @inject(alembic_cfg=AlembicConfiguration)
    def call_alembic(self, args, alembic_cfg):
        # type: (List[str], AlembicConfiguration)->None
        is_initializing = len(args) and args[0] == 'init'
        alembic_directory = alembic_cfg.alembic_directory
        if is_initializing:
            cwd = None
            args.append(alembic_directory)
        else:
            cwd = os.getcwd()
            os.chdir(alembic_directory)
        CommandLine().main(args)
        if is_initializing:
            default_ini_path = 'alembic.ini'
            target_ini_path = os.path.join(alembic_directory, 'alembic.ini')
            os.rename(default_ini_path, target_ini_path)
        else:
            os.chdir(cwd)

    def __call__(self, *args, **kwargs):
        self._alembic()


class AlembicModule(Module):
    """Adds Alembic support for migrations."""

    ALEMBIC_CONFIG_NAME = 'ALEMBIC'

    @provides(AlembicConfiguration)
    @inject(config=Config)
    def provide_alembic_configuration(self, config):
        # type: (Config) -> AlembicConfiguration
        return config.get(AlembicModule.ALEMBIC_CONFIG_NAME)

    def configure(self, binder):
        # type: (Binder) -> None
        simple_bind(binder, AlembicCli, singleton)
