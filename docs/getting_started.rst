Getting started
===============

Installation
------------

We recommend to install it trough `PyPi <https://pypi.org/>`_ and
run it in a `virtualenv <https://docs.python.org/3/library/venv.html>`_ or
`docker <https://www.docker.com/>`_ container.

.. code-block:: console

    $ pip install zsl


Hello world app
---------------

For now it is a bit cumbersome to get it running. It has inherited settings
trough ENV variables from Flask and has a rigid directory structure like django
apps. On top of that, it needs a database and redis.

The minimum application layout has to contain:

.. code-block:: console

    .
    ├── app                    # application sources
    │   ├── __init__.py
    │   └── tasks              # public tasks
    │       ├── hello.py
    │       └── __init__.py
    ├── settings               # settings
    │   ├── app_settings.cfg
    │   ├── default_settings.py
    │   └── __init__.py
    └── tests

.. code-block:: console

    $ export ZSL_SETTINGS=`pwd`/settings/app_settings.cfg

The minimum configuration has to contain these values:

::

    # settings/app_settings.cfg

    TASKS = TaskConfiguration()\
        .create_namespace('task')\
            .add_packages(['app.tasks'])\
            .get_configuration()
    RESOURCE_PACKAGE = ()
    DATABASE_URI = 'postgresql://postgres:postgres@localhost/postgres'
    DATABASE_ENGINE_PROPS = {}
    SERVICE_INJECTION = ()
    REDIS={
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    RELOAD=True

::

    # hello.py

    class HelloWorldTask(object):
        def perform(self, data):
            return "Hello World"

.. code-block:: console

    $ python -m zsl web
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

.. code-block:: console

    $ curl http://localhost:5000/task/hello/hello_world_task
    Hello world!
