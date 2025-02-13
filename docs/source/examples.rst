.. _examples:

Usage Examples
====================================

To better understand what ``pyscx`` is, we will provide simple examples that reflect
the core essence and some practical features of using the library.

In addition to this documentation, code examples can be found here: `GitHub Examples <https://github.com/Oidaho/pyscx/tree/main/examples>`_

Token redefinition
------------------------------------

If there is a need to send a request with a token different from the one provided during
the initialization of the :class:`API` class, you can do so by passing the token
through **\*\*kwargs**:

.. code-block:: python

    import os
    from dotenv import load_dotenv

    from pyscx import Server, API
    from pyscx.token import Token, TokenType


    load_dotenv()

    user_token = Token(
        value=os.getenv("DEMO_USER_ACCESS_TOKEN"),
        type=TokenType.USER,
    )


    api = API(server=Server.DEMO, tokens=user_token)

    clan_list = api.friends(region="EU").get_all(token="other_user_token")


.. warning::
    Be mindful of which token you pass to the method.
    Each method requires an access token of its specific type.

Different number of tokens
------------------------------------

You can pass only one token or two tokens to the :class:`API` class.
Alternatively, you can choose not to pass any tokens at all. In this case,
methods that require a token type will raise an exception. However, as we've seen earlier,
a token can also be sent directly through the request.

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


    user_api = API(server=Server.DEMO, tokens=user_token)
    app_api = API(server=Server.DEMO, tokens=app_token)

    api = API(server=Server.DEMO, tokens=[user_token, app_token])


    clan_list1 = user_api.friends(region="EU").get_all()
    clan_list2 = api.friends(region="EU").get_all()

    print(clan_list1 == clan_list2) # True
    

