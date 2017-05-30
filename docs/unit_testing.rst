Unit testing
############

Create unit tests so that each test is a subclass of :class:`unittest.TestCase` from Python's
`unittest <https://docs.python.org/3/library/unittest.html>`_ library as usual. A good practice is to place the tests
into `tests` package in your root application package. And then it's all up to the developers and we provide some
hints.

There are various choices how to test and what to test regarding Zsl apps.

First of all, if you do not need a ZSL instance, do not create it and run the unit tests without the instance. It will
speed the things up. If you really need it see the section about
:ref:`unit-testing-zsl-instance`.

Running the unit tests
======================

To run all the unit tests in the package `<app_root_package>.tests` run the following.

.. code-block:: console

    $ cd <app_root_package>/.. # To the directory where the application root package is.
    $ python -m unittest discover <app_root_package>.tests '*_test.py'

See the `example project tests <https://github.com/AtteqCom/zsl_examples/tree/master/time_tracker/time_tracker/tests>`_
on how to use the tests.

There are various test mixins that could be used while testing.

.. _unit-testing-zsl-instance:

Testing with a Zsl instance
---------------------------

We show an example test case which can be reused.

.. code-block:: python

    class ToBeTestedTaskTestCase(ZslTestCase, HttpTestCase, TestCase):
        ZSL_TEST_CONFIGURATION = ZslTestConfiguration(app_name='time_tracker', container=WebContainer, version=None,
                                                      profile=None)


Add :class:`zsl.unittest.zsl.ZslTestCase` mixin to your tests so that the `setUpClass` method is run during the test
class initialization phase. This means `ZslTestCase` must be before `unittest.TestCase`.

Define the Zsl instance which should be created using `ZSL_TEST_CONFIGURATION` member of the test case which is of type
:class:`zsl.unittest.zsl.ZslTestConfiguration`. This allows to set up the application name, container and modules to be
used, version and the test profile/settings.

Testing with HTTP requests to tasks
-----------------------------------

Add :class:`zsl.unittest.http.HTTPTestCase` mixin to your class and you can use various methods to simplify your tests.
To make mock web requests on your configuration you may use the following.

.. code-block:: python

    with self.getHTTPClient() as client:
        DATA = {
            'test-data': 'the to be tested task just returns a copy'
        }

        rv = self.requestTask(client, '/task/to_be_tested_task', DATA)
        self.assertHTTPStatus(http.client.OK, rv.status_code, "OK status is expected.")
        self.assertJSONData(rv, DATA, "Correct data copy must be returned.")


Method `getHTTPClient` returns an object which is able to make requests to the current configuration. However to speed
thinks up one may use methods `requestTask` which will make a POST request using the given client to the given URL with
the given data.

Then one may assert the status codes and the returned data. To inspect data on your own just use `extractResponseJSON`.

Testing with database
---------------------

Use :class:`zsl.unittest.http.DbTestCase` mixin which adds you the possibility to create database from scratch using
`createSchema` method.