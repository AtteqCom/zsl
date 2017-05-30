Unit testing
############

Create unit tests so that each test is a subclass of :class:`unittest.TestCase` from Python's
`unittest <https://docs.python.org/3/library/unittest.html>`_ library.

There are various choices how to test. First of all, if you do not need a ZSL instance, do not create it and run
the unit tests without it. It will speed the things up.

Running the unit tests
======================

See the example project on how to use the tests.

There are various test mixins that could be used while testing.

Testing with a Zsl instance
---------------------------

Testing with HTTP requests to tasks
-----------------------------------

Testing with database
---------------------

