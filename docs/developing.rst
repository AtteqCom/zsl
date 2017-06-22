Developing ZSL
##############

Documentation
=============

Creating the documentation is easy. The requirements for generating
documentation are in `documentation` extra of `zsl`. Just install
`sphinx` and the mentioned dependencies if required and perform
the following.

.. code-block:: console

    $ tox -e docs

Running ZSL unit tests
======================

To run all of the ZSL unit tests one should start

.. code-block:: console

    $ tox

To run only a selected test, e.g. tests in :mod:`tests.resource.guarded_resource_test`:

.. code-block:: console

    $ cd zsl
    $ python -m unittest tests.resource.guarded_resource_test

