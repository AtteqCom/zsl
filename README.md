[![Build Status](https://travis-ci.org/AtteqCom/zsl.svg?branch=master)](https://travis-ci.org/AtteqCom/zsl)
[![Coverage Status](https://coveralls.io/repos/github/AtteqCom/zsl/badge.svg?branch=master)](https://coveralls.io/github/AtteqCom/zsl?branch=master)

# ZSL - z' service layer

ZSL is a Python micro-framework utilizing
[dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
for creating service applications on top of
[Flask](http://flask.pocoo.org/docs/0.12/) web framework and
[Gearman](http://gearman.org/) job server or
[Celery](http://http://www.celeryproject.org/) task queue.

## Motivation

We developed ZSL to modernize our workflow with maintaining our clients'
mostly web applications written in various older CMS solutions without the
need to rewrite them significantly. With ZSL we can write our new components
in Python, with one coherent shared codebase, accessible trough Gearman or
JavaScript. Also the same code can be called through various endpoints - web or
 task queue nowadays.

## Disclaimer

At current stage this should be taken as proof of concept. We don't recommend to
run in any production except ours. It is too rigid, with minimum test coverage
and lots of bad code practices. We open sourced it as way of motivation for us
to make it better.

## Installation

We recommend to install it trough [PyPi](https://pypi.org/) and run it in
a [virtualenv](https://docs.python.org/3/library/venv.html) or
[docker](https://www.docker.com/) container.

```bash
$ pip install zsl
```

## Getting started

For now it is a bit cumbersome to get it running. It has inherited settings
trough ENV variables from Flask and has a rigid directory structure like django
apps. On top of that, it needs a database and Redis.

The minimum application layout has to contain:
```
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
```

```bash
$ export ZSL_SETTINGS=`pwd`/settings/app_settings.cfg
```

```python
# settings/app_settings.cfg

TASKS = TaskConfiguration()\
        .create_namespace('task')\
            .add_packages(['app.tasks'])\
            .get_configuration()
RESOURCE_PACKAGE = ()
DATABASE_URI = 'postgresql://postgres:postgres@localhost/postgres'
DATABASE_ENGINE_PROPS = {}
SERVICE_INJECTION = ()
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}
RELOAD = True

```

```python
# hello.py

class HelloWorldTask(object):
    def perform(self, data):
        return "Hello World"
```

```bash
$ python -m zsl web
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

```bash
$ curl http://localhost:5000/task/hello/hello_world_task
Hello world!
```
