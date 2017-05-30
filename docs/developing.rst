Developing ZSL
##############

Documentation
=============

Creating the documentation is easy. The requirements for generating
documentation are in `documentation` extra of `zsl`. Just install
`sphinx` and the mentioned dependencies if required and perform
the following.

.. code-block:: console

    $ pip install sphinx recommonmark sphinx_rtd_theme
    $ cd docs
    $ make
