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

* ``TASK_PACKAGES``
  List of packages with tasks. The task router will search any task in these
  packages with given order.

* ``RESOURCE_PACKAGES``
  List of packages with resources. The resource router will search any resource
  in these packages with given order.

* ``DATABASE_URI``
  Database URL for `SQLAlchemy <http://sqlalchemy.org>`_'s
  `crate_engine <http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine>`_.

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
  Set the debug mode.

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
  The dictionary containing the default CORS/crossdomain settings.
  The only available options for now are:
    * ``origin`` - with the allowed origin.
