.. _reference:

Package Reference 
====================================

This section provides a description of all the classes you will encounter while using **pyscx**.

.. note::
    **"Our task is to invent. Yours is to use." © Oidaho**

.. warning::
    Before you dive into the documentation, we strongly recommend reviewing the :ref:`examples` section.
    By looking at the practical use of **pyscx**, it will be easier to navigate the :ref:`reference`.


------------------------------------

API
------------------------------------

The core and fundamental entity in **pyscx** is the :class:`API` class.
This class provides access to the STALCRAFT:X API with automatic handling
of different types of authorization tokens.

The :class:`pyscx.api.API` class offers a convenient interface for calling API methods,
somewhat resembling a builder pattern, although it is not strictly an implementation of it.

.. autoclass:: pyscx.api.API
    :members:
    :undoc-members:
    :show-inheritance:
    :special-members: __init__,__getattribute__
    :no-index:

In this class, the query-building function is handled by the :func:`API.__getattribute__`
method. If an attribute is accessed that doesn't exist in the class,
the :func:`API.__getattribute__` method interprets this as an **attempt
to access a specific API methods group** (:class:`MethodsGroup`).
In this case, the attribute name will correspond to the name of the API method group.

------------------------------------

Token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GitHub Database
------------------------------------

.. danger::
    The functionality related to this section is under development.

------------------------------------

Async API
------------------------------------

.. danger::
    The functionality related to this section is under development.