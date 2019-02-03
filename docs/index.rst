.. zsl documentation master file, created by
   sphinx-quickstart on Tue Dec 20 16:26:44 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ZSL - z' service layer
======================

ZSL is a Python 2.7 micro-framework utilizing
`dependency injection <https://en.wikipedia.org/wiki/Dependency_injection>`_
for creating service applications on top of `Flask <http://flask.pocoo.org/docs/0.12/>`_
and `Gearman <http://gearman.org/>`_ job server.

Motivation
##########

We developed ZSL to modernize our workflow with maintaining our clients web
applications written in various older CMS solutions without the need to rewrite
them significantly. With ZSL we can write our new components in python, with one
coherent shared codebase, accessible trough Gearman or JavaScript.

Disclaimer
##########

At current stage this should be taken as proof of concept. We don't recommend to
run in any production except ours. It is too rigid, with minimum test coverage
and lots of bad code practices. We open sourced it as way of motivation for us
to make it better.

.. toctree::
   :glob:
   :maxdepth: 1

   getting_started
   configuration
   modules_and_containers
   error_handling
   unit_testing
   extending
   message_queues
   caching
   database
   api
   developing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
