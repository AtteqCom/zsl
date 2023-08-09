Database
########

Using DB Sessions in Services
=============================
.. automodule:: zsl.service.service
    :members:

DB sessions are closely tied to individual service instances. As a result, initiating transactions across different services is discouraged. This practice can lead to nested transactions, complicating debugging and potentially causing data inconsistencies. Ensure that transactions are completed within their original context to maintain clarity and stability.

For managing database sessions and transactions in your services, we provide two main utilities: a context manager ``tx_session`` and a method decorator ``transactional``.

Using ``tx_session``
--------------------

The ``tx_session`` is a context manager that can be used with Python's ``with`` statement. It manages the creation, commit, and closure of a database session.

**Example:**

.. code-block:: python

   from zsl.service import tx_session

   class MyService(Service):
       def my_method(self):
           with tx_session(self) as session:
               self._repository.create(session, 2, 3, 4)

**Explanation:**

In the code above, the database session is automatically opened when entering the ``with`` block and committed (if there's no exception) and closed when exiting the ``with`` block.

Using ``transactional``
-----------------------

The ``transactional`` is a decorator which makes the entire function transactional. It essentially wraps the function within a ``tx_session`` to manage the session lifecycle.

**Example:**

.. code-block:: python

   from zsl.service import transactional

   class MyService(Service):
       @transactional
       def my_function(self):
           self._repository.create(self._orm, 2, 3, 4)

**Explanation:**

Here, by annotating ``my_function`` with ``@transactional``, the entire function body becomes a transaction. The session is opened before the method logic starts and committed and closed after the method completes (or rolled back if there's an exception).
