import os

import pytest
from dotenv import load_dotenv
from requests.exceptions import HTTPError

from pyscx import API, Server
from pyscx.exceptions import MissingTokenError
from pyscx.token import Token, TokenType

load_dotenv()


def get_token(env_var: str, token_type: TokenType) -> Token:
    return Token(value=os.getenv(env_var), type=token_type)


API_METHODS_TEST_CASES = [
    ("regions", "get_all", {}),
    ("emissions", "get_info", {}),
    ("friends", "get_all", {"character_name": "Test-1"}),
    ("auction", "get_item_history", {"item_id": "1kv2"}),
    ("auction", "get_item_lots", {"item_id": "1kv2"}),
    ("characters", "get_all", {}),
    ("characters", "get_profile", {"character_name": "Test-1"}),
    ("clans", "get_info", {"clan_id": "647d6c53-b3d7-4d30-8d08-de874eb1d845"}),
    ("clans", "get_members", {"clan_id": "647d6c53-b3d7-4d30-8d08-de874eb1d845"}),
    ("clans", "get_all", {}),
]


@pytest.mark.parametrize(
    "group, method, kwargs",
    API_METHODS_TEST_CASES,
    ids=[f"{g}.{m}()" for g, m, _ in API_METHODS_TEST_CASES],
)
def test_api_method(group, method, kwargs):
    """Test API groups and their methods."""
    app_token = get_token("DEMO_APP_ACCESS_TOKEN", TokenType.APPLICATION)
    user_token = get_token("DEMO_USER_ACCESS_TOKEN", TokenType.USER)

    api = API(server=Server.DEMO, tokens=[user_token, app_token])

    api_group = getattr(api, group)(region="EU")
    getattr(api_group, method)(**kwargs)


def test_token_incorrect_redefinition():
    """Ensure using an application token for user-specific methods raises PermissionError."""
    user_token = get_token("DEMO_USER_ACCESS_TOKEN", TokenType.USER)

    api = API(server=Server.DEMO, tokens=user_token)

    with pytest.raises(HTTPError) as exc_info:
        api.friends(region="EU").get_all(
            character_name="Test-1", token=os.getenv("DEMO_APP_ACCESS_TOKEN")
        )

    assert exc_info.type is HTTPError


def test_token_correct_redefinition():
    """Ensure using an new user token for user-specific methods does not raises PermissionError."""
    user_token = get_token("DEMO_USER_ACCESS_TOKEN", TokenType.USER)

    api = API(server=Server.DEMO, tokens=user_token)

    api.friends(region="EU").get_all(
        character_name="Test-1", token=os.getenv("DEMO_USER_ACCESS_TOKEN")
    )


@pytest.mark.parametrize(
    "env_var, token_type",
    [
        ("DEMO_USER_ACCESS_TOKEN", TokenType.APPLICATION),
        ("DEMO_APP_ACCESS_TOKEN", TokenType.USER),
    ],
    ids=["App_Instead_User", "User_Instead_App"],
)
def test_token_with_invalid_type(env_var, token_type):
    user_token = get_token(env_var, token_type)

    api = API(server=Server.DEMO, tokens=user_token)

    with pytest.raises(MissingTokenError) as exc_info:
        if token_type == TokenType.APPLICATION:
            api.friends(region="EU").get_all(character_name="Test-1")
        else:
            api.clans(region="EU").get_all()

    assert exc_info.type is MissingTokenError
