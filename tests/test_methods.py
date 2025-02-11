import os

import pytest
from dotenv import load_dotenv
from pyscx import API, Server
from pyscx.token import Token, TokenType

load_dotenv()


def get_token(env_var: str, token_type: TokenType) -> Token:
    return Token(value=os.getenv(env_var), type=token_type)


app_token = get_token("DEMO_APP_ACCESS_TOKEN", TokenType.APPLICATION)
user_token = get_token("DEMO_USER_ACCESS_TOKEN", TokenType.USER)

api = API(server=Server.DEMO, tokens=[user_token, app_token])

API_TEST_CASES = [
    ("regions", "get_all", {}),
    ("emissions", "get_info", {"region": "RU"}),
    ("friends", "get_all", {"region": "EU", "character_name": "Test-1"}),
    ("auction", "get_item_history", {"region": "EU", "item_id": "1kv2"}),
    ("auction", "get_item_lots", {"region": "EU", "item_id": "1kv2"}),
    ("characters", "get_all", {"region": "EU"}),
    ("characters", "get_profile", {"region": "EU", "character_name": "Test-1"}),
    ("clans", "get_info", {"region": "EU", "clan_id": "647d6c53-b3d7-4d30-8d08-de874eb1d845"}),
    ("clans", "get_members", {"region": "EU", "clan_id": "647d6c53-b3d7-4d30-8d08-de874eb1d845"}),
    ("clans", "get_all", {"region": "EU"}),
]


@pytest.mark.parametrize(
    "group, method, kwargs",
    API_TEST_CASES,
    ids=[f"{g}.{m}()" for g, m, _ in API_TEST_CASES],
)
def test_api_method(group, method, kwargs):
    """Test API groups and their methods."""
    api_group = getattr(api, group)
    getattr(api_group, method)(**kwargs)


def test_token_redefinition():
    """Ensure using an application token for user-specific methods raises PermissionError."""
    with pytest.raises(PermissionError, match=".*only available.*") as exc_info:
        api.friends.get_all(
            region="EU", character_name="Test-1", token=os.getenv("DEMO_APP_ACCESS_TOKEN")
        )

    assert exc_info.type is PermissionError
