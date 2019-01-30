Configuration
#############

A global configuration is required to exists as a package
``settings.default_settings``. Per-installation/environment configuration is possible.
A file with suffix `cfg` and name set in environment variable ``ZSL_SETTINGS`` is needed.

Environment variables
---------------------

* ``ZSL_SETTINGS``
  Location of the per-installation configuration file (with \*.cfg suffix).

Required fields
---------------

* ``TASKS``
  The task router will search for task according to the task configuration.
  The object under this variable is an instance of
  :class:`zsl.router.task.TaskConfiguration`. The users register the packages
  holding task classes under their urls. See the example app and the following
  example for more.

  If we have a ``FooApiTask`` in module ``myapp.tasks.api.v1.foo_api_task``, then
  we register it under url `/api/v1` in so that we use::

    TASKS = TaskConfiguration()\
      .create_namespace('api/v1')\
        .add_packages(['myapp.tasks.api.v1'])\
        .get_configuration()

  Notice that all the tasks in the modules in the package
  ``myapp.tasks.api.v1.foo_api_task`` will be routed under `/api/v1` url. If one needs
  a more detailed routing, then ``add_routes`` method is much more convenient.

* ``RESOURCE_PACKAGES``
  List of packages with resources. The resource router will search any resource
  in these packages with given order.

* ``DATABASE_URI``
  Database URL for `SQLAlchemy <https://www.sqlalchemy.org/>`_'s
  `crate_engine <https://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine>`_.

* ``DATABASE_ENGINE_PROPS``
  A dictionary of optional properties for the DB connection.

* ``SERVICE_INJECTION``
  List of services initialized and bind to the injecor after start.::

      SERVICE_INJECTION = ({
          'list':  ['AccountService', 'BuildService']
          'package': 'app.services'
      })

* ``REDIS``
  `Redis <https://redis-py.readthedocs.io/en/latest/#redis.Redis>`_ configuration.

Optional fields
---------------

* ``RELOAD``
  Reload tasks on every call. Especially usable when debugging.

* ``DEBUG``
  Set the debug mode - ``True`` or ``False``.

* ``LOGGING``
  Logging settings are specified in `LOGGING` variable as a python dictionary.
  ZSL uses python logging as the logging infrastructure and the configuration
  is done accordingly.

  The concrete options are specified in Python Logging library in the part
  called dictionary configuration, just check the `logging.config
  <https://docs.python.org/3/library/logging.config.html#module-logging.config>`_
  module documentation for more. An example is here.::

    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(levelname)s %(name)s %(asctime)-15s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
        },
        'loggers': {
            'storage': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }

  Because of using Flask one has to provide `import_name` parameter to the
  :class:`zsl.application.service_application.ServiceApplication` object
  constructor. This `import_name` is also the name of the root logger used
  in the application. Thus it is convenient to choose as the root package
  name of the project.


* ``EXTERNAL_LIBRARIES``
  Add external libraries to path. This option will be deprecated
  use a correct virtualenv environment instead.::

      EXTERNAL_LIBRARIES = {
          'vendor_path': './vendor'
          'libs': ['my_lib_dir1', 'my_lib_dir2']
      }

* ``CORS``
  The configuration containing the default CORS/crossdomain settings. Check
  :class:`zsl.application.modules.web.cors.CORSConfiguration`. The available
  options are:

    * `origin`,
    * `allow_headers`,
    * `expose_headers`,
    * `max_age`.

  Check CORS explanation on `Wikipedia <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`_.
