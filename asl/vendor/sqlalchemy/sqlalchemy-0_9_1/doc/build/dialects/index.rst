.. _dialect_toplevel:

Dialects
========

The **dialect** is the system SQLAlchemy uses to communicate with various types of :term:`DBAPI` implementations and databases.
The sections that follow contain reference documentation and notes specific to the usage of each backend, as well as notes
for the various DBAPIs.

All dialects require that an appropriate DBAPI driver is installed.

Included Dialects
-----------------

.. toctree::
    :maxdepth: 1
    :glob:

    drizzle
    firebird
    mssql
    mysql
    oracle
    postgresql
    sqlite
    sybase

.. _external_toplevel:

External Dialects
-----------------

.. versionchanged:: 0.8
   As of SQLAlchemy 0.8, several dialects have been moved to external
   projects, and dialects for new databases will also be published
   as external projects.   The rationale here is to keep the base
   SQLAlchemy install and test suite from growing inordinately large.

   The "classic" dialects such as SQLite, MySQL, Postgresql, Oracle,
   SQL Server, and Firebird will remain in the Core for the time being.

Current external dialect projects for SQLAlchemy include:

Production Ready
^^^^^^^^^^^^^^^^

* `ibm_db_sa <http://code.google.com/p/ibm-db/wiki/README>`_ - driver for IBM DB2 and Informix, developed jointly by IBM and SQLAlchemy developers.
* `sqlalchemy-sqlany <https://github.com/sqlanywhere/sqlalchemy-sqlany>`_ - driver for SAP Sybase SQL Anywhere, developed by SAP.
* `sqlalchemy-monetdb <https://github.com/gijzelaerr/sqlalchemy-monetdb>`_ - driver for MonetDB.

Experimental / Incomplete
^^^^^^^^^^^^^^^^^^^^^^^^^^

Dialects that were started but are not in a completed state.  Code contributions
welcome here.

* `CALCHIPAN <https://bitbucket.org/zzzeek/calchipan/>`_ - Adapts `Pandas <http://pandas.pydata.org/>`_ dataframes to SQLAlchemy.
* `sqlalchemy-akiban <https://github.com/zzzeek/sqlalchemy_akiban>`_ - driver and ORM extensions for the `Akiban <http://www.akiban.com>`_ database.
* `sqlalchemy-cubrid <https://bitbucket.org/zzzeek/sqlalchemy-cubrid>`_ - driver for the CUBRID database.

Attic
^^^^^

Dialects in the "attic" are those that were contributed for SQLAlchemy long ago
but have received little attention or demand since then, and are now moved out to
their own repositories in at best a semi-working state.
Community members interested in these dialects should feel free to pick up on
their current codebase and fork off into working libraries.

* `sqlalchemy-access <https://bitbucket.org/zzzeek/sqlalchemy-access>`_ - driver for Microsoft Access.
* `sqlalchemy-informixdb <https://bitbucket.org/zzzeek/sqlalchemy-informixdb>`_ - driver for the informixdb DBAPI.
* `sqlalchemy-maxdb <https://bitbucket.org/zzzeek/sqlalchemy-maxdb>`_ - driver for the MaxDB database


