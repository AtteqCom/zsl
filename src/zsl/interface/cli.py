"""
:mod:`zsl.interface.cli`
------------------------

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>

The module is responsible for creating the CLI interface of ZSL and provides the main `click` group for all the CLI
commands and groups. If any command is to be added add it to this group `cli` defined in this module.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import *
import sys

import click

from zsl.version import version

click.disable_unicode_literals_warning = True


def _get_version(ctx, _, value):
    """Click callback for option to show current ZSL version."""

    if not value or ctx.resilient_parsing:
        return
    message = 'Zsl %(version)s\nPython %(python_version)s'
    click.echo(message % {
        'version': version,
        'python_version': sys.version,
    }, color=ctx.color)
    ctx.exit()


@click.group(help="ZSL CLI toolkit")
@click.option('--version', help="Show ZSL version", expose_value=False,
              is_flag=True, is_eager=True, callback=_get_version)
def cli():
    """The command group for ZSL."""
    pass


@cli.command(help="Open interactive shell (bpython) with the ZSL environment",
             context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def shell(args):
    import bpython
    bpython.embed(args=list(args))
