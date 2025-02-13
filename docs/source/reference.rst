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

The :class:`API` class offers a convenient interface for calling API methods,
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

The :class:`Token` class serves as an interface for conveniently passing access tokens
to the :class:`API` class. It allows you to define standard access tokens for
the :class:`API` class in a clean, concise, and understandable manner, which will
be **automatically** used by the class when calling API methods.

.. autoclass:: pyscx.token.Token
    :undoc-members:
    :show-inheritance:
    :special-members: __init__
    :no-index:

To definitively specify the type of the token being used,
the :class:`TokenType` class is provided, which inherits from :class:`Enum`.

.. autoclass:: pyscx.token.TokenType
    :undoc-members:
    :members:
    :show-inheritance:
    :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

API Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For your convenience and ease of working with the data you will receive from the
STALCRAFT:X API, models have been implemented to wrap raw data into Python objects.

These models are implemented using the ``Pydantic`` library. Therefore,
hey inherit all the functionality offered by the :class:`BaseModel` class
from ``Pydantic``. The :class:`APIObject` class is created based on the
:class:`BaseModel`, and all other representations inherit from it.

.. autoclass:: pyscx.objects.APIObject
    :undoc-members:
    :members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. note::
    The documentation for the :func:`raw` function states that it returns the data
    in its original form. This means that the case of the keys in the data dictionary and
    the value formats will be restored to their original, and any fields with the value ``None``
    will be removed.

All API objects can be divided into specific groups, which reflect the general association
of models with a particular method or set of API methods.

Regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.objects.Region
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

Emissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.objects.Emission
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

Auction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.objects.AuctionLot
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.AuctionRedeemedLot
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

Clans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.objects.Clan
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.ClanMemberRank
    :undoc-members:
    :members:
    :show-inheritance:
    :no-index:

.. autoclass:: pyscx.objects.ClanMember
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.objects.CharacterStatType
    :undoc-members:
    :members:
    :show-inheritance:
    :no-index:

.. autoclass:: pyscx.objects.CharacterStat
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.CharacterMeta
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.CharacterClan
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.CharacterInfo
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

.. autoclass:: pyscx.objects.FullCharacterInfo
    :undoc-members:
    :show-inheritance:
    :exclude-members: model_config
    :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

API Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you attempt to access the :class:`API` class in an effort to call an API method,
the code structure will likely look something like this:

.. code-block:: python

    api.clans("EU").get_all()

In this case, the following will happen:

1. You will attempt to access the ``regions`` attribute.
2. The :func:`__getattribute__` method will not find an attribute named ``regions`` and will return an **instance** of the method group factory class (:class:`MethodsGroupFabric`).
3. The :func:`__call__` method of the :class:`MethodsGroupFabric` class will be invoked, after which an instance of the :class:`MethodsGroup` class will be returned with the **region** pre-set.
4. The :func:`get_all` method will be called on the instance of the :class:`MethodsGroup`, which retrieves the list of all game regions.

.. autoclass:: pyscx.methods.MethodsGroup
    :undoc-members:
    :show-inheritance:
    :no-index:

Naturally, this sequence of actions is a generalization.
In practice, you will receive instances of classes that inherit from :class:`MethodsGroup`.
These instances will contain methods related to a specific group of the API.

Regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.RegionsMethods
    :members:
    :show-inheritance:
    :no-index:

Emissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.EmissionsMethods
    :members:
    :show-inheritance:
    :no-index:

Friends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.FriendsMethods
    :members:
    :show-inheritance:
    :no-index:

Auction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.AuctionMethods
    :members:
    :show-inheritance:
    :no-index:

Clans
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.ClansMethods
    :members:
    :show-inheritance:
    :no-index:

Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyscx.methods.CharactersMethods
    :members:
    :show-inheritance:
    :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Items Database
------------------------------------

.. danger::
    The functionality related to this section is under development.

------------------------------------

Async API
------------------------------------

.. danger::
    The functionality related to this section is under development.