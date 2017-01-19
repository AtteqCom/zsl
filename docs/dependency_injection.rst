Dependency injection
====================

ZSL uses `flask injector <https://github.com/alecthomas/flask_injector>`_, but
with some customizations.

For simple application the use-case will be usually trough ``inject``.

.. code-block:: python
   :emphasize-lines: 1,5

    from injector import inject
    from zsl.application.service_application import AtteqServiceFlask

    class VersionTask(object):
        @inject(app=AtteqServiceFlask)
        def perform(self, app):
            return app.VERSION

At start ZSL injects these objects

* ``zsl.application.service_application.AtteqServiceFlask``
  ZSL application object, which is extended upon Flask app.

* ``flask.config.Config``
  Flask's config object.
