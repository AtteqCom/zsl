Configuration
=============

A global configuration is required to exists as a package
``settings.default_settings``. Per-installation configuration file set in ENV
variable ``APP_SETTINGS`` is also needed.

Environment variables
---------------------

* ``APPLICATION_PACKAGE_PATH``
  Location of the application sources.

* ``ASL_SETTINGS``
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
  Reload tasks on every call.

* ``DEBUG``
  Set debug mode.

* ``LOG``
  Setting for specific logger.::

      LOG = {
          'sqlalchemy.engine': {
              # settings for sqlaclhemy logger
              'handlers': ['out-handler', 'err-handler'],
              'level': 'WARNING'
          }
      }

* ``LOGGER_NAME``
  Name of tha application logger.

* ``LOG_HANDLERS``
  List of log handlers. 

* ``EXTERNAL_LIBRARIES``
  Add external libraries to path.::

      EXTERNAL_LIBRARIES = {
          'vendor_path': './vendor'
          'libs': ['my_lib_dir1', 'my_lib_dir2']
      }
