Workers
#######

Workers serve as the backbone of distributed task execution, efficiently managing asynchronous
tasks across various processes or machines. This ensures enhanced scalability and a responsive
application experience.

ZSL furnishes developers with a worker abstraction layer that is compatible with both Celery and
Gearman task queues.

Celery Workers
**************

`Celery <https://docs.celeryq.dev>`_ is a distributed task queue that supports both real-time and scheduled tasks. It is
compatible with a variety of message brokers and backends, including RabbitMQ, Redis, and
Amazon SQS.

For seamless integration into the `zsl` framework, the module `zsl.interface.celery.worker` wraps
around the Celery worker, ensuring greater flexibility.

Celery Worker Configuration
===========================

Two Implementations:

**1. CeleryTaskQueueMainWorker**:
   Customized specifically for the ZSL framework, this worker embeds the entire lifecycle of the
   Celery app, creating an isolated environment for task handling. It is ideal for setups desiring
   direct control over the app lifecycle.

**2. CeleryTaskQueueOutsideWorker**:
   Tailored for configurations where the Celery worker's lifecycle is externally overseen (using
   commands like `celery worker` or `celery multi`). This decoupled model simplifies scaling,
   deployment, and management via native Celery utilities.

Your choice hinges on the specific app dependency injection configuration.

Using CeleryTaskQueueMainWorker
-------------------------------

.. code-block:: python

    # worker.py
    from zsl.application.modules.celery_module import CeleryCliModule, CeleryTaskQueueMainWorkerModule

    class AppWorkerContainer(CoreContainer):
        celery_cli_module = CeleryCliModule
        celery = CeleryTaskQueueMainWorkerModule

    app = Zsl('app', modules=AppWorkerContainer.modules())

Using CeleryTaskQueueOutsideWorker
----------------------------------

.. code-block:: python

    # outside_worker.py
    from zsl.application.modules.celery_module import CeleryCliModule, CeleryTaskQueueOutsideWorkerModule

    class AppWorkerContainer(CoreContainer):
        celery_cli_module = CeleryCliModule
        celery = CeleryTaskQueueOutsideWorkerModule

    app = Zsl('app', modules=AppWorkerContainer.modules())

    celery = Celery(app.config['CELERY'])

.. code-block:: bash

    # To initiate 4 workers
    $ celery multi start w1 w2 w3 w4 -A outside_worker:celery -Q worker_bees -l INFO

Celery Main Worker Application Example
======================================

worker.py
---------

.. code-block:: python

    import os
    from zsl import Zsl
    from zsl.application.containers.core_container import CoreContainer
    from zsl.application.modules.celery_module import CeleryCliModule, CeleryTaskQueueMainWorkerModule
    from zsl.application.modules.cli_module import ZslCli
    from zsl.application.service_application import set_profile
    from zsl.utils.injection_helper import inject

    # Initial injector setup
    class AppWorkerContainer(CoreContainer):
        celery_cli_module = CeleryCliModule
        celery = CeleryTaskQueueMainWorkerModule

    app = Zsl('app', modules=AppWorkerContainer.modules())

    @inject(zsl_cli=ZslCli)
    def run(zsl_cli: ZslCli) -> None:
        zsl_cli.cli()

    def main() -> None:
        run()

    if __name__ == "__main__":
        main()

settings/default_settings.py
----------------------------

.. code-block:: python

    from zsl.router.task import TaskConfiguration

    TASKS = (
        TaskConfiguration()
        .create_namespace('task')
        .add_packages(['zsl.tasks'])
        .get_configuration()
    )
    RESOURCE_PACKAGE = ()
    SERVICE_INJECTION = ()
    CELERY = {
        'broker_url': 'amqp://guest:guest@localhost:5672/',
        'result_backend': 'rpc://'
    }

.. code-block:: shell

    $ docker run --name some-rabbit -p 5672:5672 rabbitmq:3-alpine

.. code-block:: shell

    # To initiate the worker
    $ python worker.py celery worker --loglevel=INFO

ZSL Celery Task
===============

The main interaction with the worker is through the :func:`zsl.interface.celery.worker.zsl_task`
function. The app has to be initialized and celery worker running for the function to get result.
zsl_task will forward the task to the celery worker, which will try to find the task and execute.

.. autofunction:: zsl.interface.celery.worker.zsl_task

As a short example we can run this in an app shell.

.. code-block:: shell

    # To enter the app shell
    $ python worker.py shell


.. code-block:: python

    from zsl.interface.celery.worker import zsl_task

    result = zsl_task.delay({"path": "task/zsl/version_task", "data": {}})
    print(result.get())

.. code-block:: bash

    >> {'task_name': 'task/zsl/version_task', 'data': '{"ASL": "1.0.0a3", "SqlAlchemy": "2.0.21"}'}
