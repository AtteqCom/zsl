[![Build Status](https://travis-ci.org/AtteqCom/zsl.svg?branch=master)](https://travis-ci.org/AtteqCom/zsl)
[![Coverage Status](https://coveralls.io/repos/github/AtteqCom/zsl/badge.svg?branch=master)](https://coveralls.io/github/AtteqCom/zsl?branch=master)

# ZSL - z' service layer

ZSL is a Python micro-framework utilizing
[dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
for creating service applications on top of
[Flask](https://flask.palletsprojects.com/en/1.1.x/) web framework and
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

## Deploying

Deploy will happen upon pushing a new tag to Gitlab.

### Creating new tag/version

Use [bump2version](https://github.com/c4urself/bump2version) to update version in config files. It will also create commit and new tag.

```bash
$ bumpversion --new-version ${VERSION} {major|minor|patch} --tag-name ${VERSION}
```

Version name uses [semver](https://semver.org/). Starts with number.

### Pipeline

Current pipeline tries to copy previous Travis runs. It runs tox target seperately and on a tag push will create deploy.

#### Tox Docker image

Gitlab pipeline runs inside a docker image which is defined in `docker/Dockerfile.tox`. Currently we manually configure, build and push it to gitlab container registry. So to update the container follow this steps.

When pushing for the first time run, you have to create an access token and login to atteq gitlab container registry. 
Go to https://gitlab.atteq.com/atteq/z-service-layer/zsl/-/settings/access_tokens and create a token to read/write to registry. Then run

`docker login registry.gitlab.atteq.com:443`

To build/push the image:

1. Build image locally.

    `docker build -t zsl/tox-env -f docker/Dockerfile.tox`

2. Tag image.

    `docker tag zsl/tox-env registry.gitlab.atteq.com:443/atteq/z-service-layer/zsl/tox-env:latest`

3. Push image.

    `docker push registry.gitlab.atteq.com:443/atteq/z-service-layer/zsl/tox-env:latest`

4. Update image hash in `.gitlab-ci.yml`. (copy from build output or `docker images --digests`).