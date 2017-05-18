"""
:mod:`zsl.interface.run`
------------------------

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import print_function
from __future__ import unicode_literals

import click
import sys

from zsl import __version__

click.disable_unicode_literals_warning = True


def _get_version(ctx, _, value):
    """Click callback for option to show current ZSL version."""

    if not value or ctx.resilient_parsing:
        return
    message = 'Zsl %(version)s\nPython %(python_version)s'
    click.echo(message % {
        'version': __version__,
        'python_version': sys.version,
    }, color=ctx.color)
    ctx.exit()


@click.group(help="ZSL CLI toolkit")
@click.option('--version', help="Show ZSL version", expose_value=False,
              is_flag=True, is_eager=True, callback=_get_version)
def cli():
    pass


@cli.command(help="Open interactive shell (bpython) with the ZSL environment",
             context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def shell(args):
    import bpython
    bpython.embed(args=list(args))
