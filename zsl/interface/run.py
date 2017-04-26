#!/usr/bin/python
"""
:mod:`zsl.interface.run`
------------------------

.. moduleauthor:: Peter Morihladko <peter@atteq.com>, Martin Babka <babka@atteq.com>
"""
from __future__ import print_function
from __future__ import unicode_literals

import sys

import click
click.disable_unicode_literals_warning = True

from zsl import Zsl, __version__


def get_version(ctx, _, value):
    """Click callback for option to show current ZSL version."""

    if not value or ctx.resilient_parsing:
        return
    message = 'Zsl %(version)s\nPython %(python_version)s'
    click.echo(message % {
        'version': __version__,
        'python_version': sys.version,
    }, color=ctx.color)
    ctx.exit()


@click.group(help="ZSL cli toolkit")
@click.option('--version', help="Show ZSL version", expose_value=False,
              is_flag=True, is_eager=True, callback=get_version)
def cli():
    pass


@cli.group(help="run something useful")
def run():
    pass


@run.command(help="run web server and serve the application")
def web():
    from zsl.application.containers.web_container import WebContainer
    app = Zsl(__name__, modules=WebContainer.modules())
    app.run_web()


@cli.command(help="open interactive shell (bpython) with the ZSL environment",
             context_settings=dict(ignore_unknown_options=True))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def shell(args):
    import bpython
    bpython.embed(args=list(args))


@run.command(help="execute task")
@click.argument('task_path', metavar='task')
@click.argument('data', default=None, required=False)
def task(task_path, data=None):
    from zsl.interface.task import exec_task
    Zsl(__name__)
    result = exec_task(task_path, data)
    # Run the task.
    click.echo(result)


def run_celery_worker(worker_args):
    """Run Zsl celery worker.

    :param worker_args: arguments for celery worker
    """
    from zsl.application.containers.celery_container import CeleryContainer

    app = Zsl(__name__, modules=CeleryContainer.modules())

    app.run_worker(worker_args)


def run_gearman_worker():
    from zsl.application.containers.gearman_container import GearmanContainer
    print("Initializing app.")
    app = Zsl(__name__, modules=GearmanContainer.modules())
    app.run_worker()


@run.command(help="run worker",
             context_settings=dict(ignore_unknown_options=True))
@click.argument('task_queue', type=click.Choice(['celery', 'gearman']))
@click.argument('argv', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def worker(_, task_queue, argv):
    if task_queue == 'celery':
        run_celery_worker(argv)
    elif task_queue == 'gearman':
        run_gearman_worker()


@run.command(help="run unit tests")
def tests():
    from zsl.utils.testing import load_and_run_tests
    Zsl(__name__)
    load_and_run_tests()


@cli.group(help="generate something helpful")
def generate():
    pass


@generate.command(help="Export python models to Backbone.js")
@click.argument('module')
@click.argument('models', metavar="model", nargs=-1)
@click.option('--model-prefix', '-mp', help='namespace prefix for models (app.models.)')
@click.option("--collection-prefix", "-cp", help="namespace prefix for collection (App.collections.)")
@click.option("--model-fn", "-m", help="name of model constructor (MyApp.bb.Model)")
@click.option("--collection-fn", "-c", help="name of collection constructor (MyApp.bb.Collection)")
@click.option("--marker", help="marker to indicate the auto generated code")
@click.option("--integrate", "-i", help="integrate to file", is_flag=True)
@click.option('--js-file', '-j', help='path to file to integrate to')
def javascript_models(module, models, model_prefix, collection_prefix,
                      model_fn, collection_fn, marker, integrate, js_file):
    from zsl.utils.deploy.js_model_generator import generate_js_models
    Zsl(__name__)
    result = generate_js_models(module=module,
                                models=models,
                                model_prefix=model_prefix,
                                collection_prefix=collection_prefix,
                                model_fn=model_fn,
                                collection_fn=collection_fn,
                                marker=marker,
                                integrate=integrate,
                                js_file=js_file)
    click.echo(result)


@generate.command(help="generate documentation for Apiary")
def apiary_doc():
    from zsl.utils.deploy.apiari_doc_generator import generate_apiary_doc
    Zsl(__name__)
    generator = generate_apiary_doc()
    click.echo(generator.get_doc())


try:
    import gearman
except ImportError as e:
    gearman = None

if gearman:
    from zsl.interface.gearman.task_filler import exec_task_filler

    @cli.group(help='gearman commands')
    def gearman():
        pass

    @gearman.command()
    @click.argument('task_path', metavar='task')
    @click.argument('data', default=None, required=False)
    def task_filler(task_path, data):
        Zsl(__name__)
        exec_task_filler(task_path, data)

