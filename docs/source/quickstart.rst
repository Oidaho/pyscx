Quickstart
====================================

This guide will help you quickly get started with the library.

Installation
------------

To install the library, simply use **pip**:

.. code-block:: bash

    pip install pyscx

Basic Usage
------------

Once installed, you can start using the API by creating an instance of the :class:`API` class.

Example
^^^^^^^

.. code-block:: python

    import os
    from dotenv import load_dotenv

    from pyscx import Server, API
    from pyscx.token import Token, TokenType


    load_dotenv()

    app_token = Token(
        value=os.getenv("DEMO_APP_ACCESS_TOKEN"),
        type=TokenType.APPLICATION,
    )
    user_token = Token(
        value=os.getenv("DEMO_USER_ACCESS_TOKEN"),
        type=TokenType.USER,
    )


    api = API(server=Server.DEMO, tokens=[user_token, app_token])

    print(api.clans(region="EU").get_all())


.. note::

    To facilitate intuitive and efficient management of your tokens, the library utilizes the :class:`Token` and
    :class:`TokenType` classes.
