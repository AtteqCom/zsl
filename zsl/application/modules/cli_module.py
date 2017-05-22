from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import logging

import click
from injector import Module, singleton, Binder

from zsl.interface.cli import cli
from zsl import inject
from zsl.utils.injection_helper import simple_bind
from zsl.utils.testing import load_and_run_tests


class ZslCli(object):
    def __init__(self):
        # type: () -> ZslCli
        logging.getLogger(__name__).debug("Creating ZSL CLI.")
        self._cli = cli

    @property
    def cli(self):
        # type: () -> ZslCli
        return self._cli

    def __call__(self, *args, **kwargs):
        # type: () -> None
        cli(**kwargs)


class ZslTaskCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> ZslTaskCli
        @zsl_cli.cli.command(help="Execute a single task.")
        @click.argument('task_path', metavar='task')
        @click.argument('data', default=None, required=False)
        def task(task_path, data=None):
            from zsl.interface.task import exec_task
            result = exec_task(task_path, data)
            click.echo(result)


class ZslTestCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> ZslTestCli
        @zsl_cli.cli.group(help="Perform unit tests.")
        def test():
            pass

        @test.command(help="run test")
        def run():
            load_and_run_tests()
            pass


class ZslGenerateCli(object):
    @inject(zsl_cli=ZslCli)
    def __init__(self, zsl_cli):
        # type: (ZslCli) -> ZslGenerateCli
        @zsl_cli.cli.group(help="Perform unit tests.")
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
            generator = generate_apiary_doc()
            click.echo(generator.get_doc())


class CliModule(Module):
    """Adds Alembic support for migrations."""

    def configure(self, binder):
        # type: (Binder) -> None
        bindings = [ZslCli, ZslTaskCli, ZslTestCli, ZslGenerateCli]
        for binding in bindings:
            simple_bind(binder, binding, singleton)
