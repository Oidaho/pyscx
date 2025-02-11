from typing import Any

import pytest


TestData = dict[str, Any]


@pytest.fixture
def valid_region_data() -> TestData:
    """Демонстрационные данные с демо-сервера STALCRAFT:X API.
    Получены, путем отправки GET запроса к ресурсу `/regions`
    """
    return {"id": "RU", "name": "RUSSIA"}


@pytest.fixture
def valid_emission_data() -> TestData:
    return {
        "currentStart": "2019-08-24T14:15:22Z",
        "previousStart": "2019-08-24T14:15:22Z",
        "previousEnd": "2019-08-24T14:15:22Z",
    }


@pytest.fixture
def valid_redeemed_lot_data() -> TestData:
    return {
        "amount": 1,
        "price": 1000,
        "time": "2025-02-11T02:48:47.001594Z",
        "additional": {},
    }


@pytest.fixture
def valid_active_lot_data() -> TestData:
    return {
        "itemId": "1kv2",
        "amount": 1,
        "startPrice": 100,
        "buyoutPrice": 10000,
        "startTime": "2025-02-11T00:49:55.603680Z",
        "endTime": "2025-02-11T12:49:55.603683Z",
        "additional": {},
    }


# ! Data cannot be retrieved from the Demo API. Improvisation, see issue #11
@pytest.fixture
def valid_character_profile_data() -> TestData:
    return {
        "username": "Test-1",
        "uuid": "5c7e0994-bc22-4190-9774-5f197b1500e6",
        "status": "offline",
        "alliance": "duty",
        "lastLogin": "2019-08-24T14:15:22Z",
        "displayedAchievements": ["playtime"],
        "clan": {
            "info": {
                "id": "string",
                "name": "string",
                "tag": "string",
                "level": 0,
                "levelPoints": 0,
                "registrationTime": "2019-08-24T14:15:22Z",
                "alliance": "string",
                "description": "string",
                "leader": "string",
                "memberCount": 0,
            },
            "member": {"name": "Test-1", "rank": "RECRUIT", "joinTime": "2019-08-24T14:15:22Z"},
        },
        "stats": [{"id": "string", "type": "INTEGER", "value": {}}],
    }


@pytest.fixture
def valid_user_character_data() -> TestData:
    return {
        "information": {
            "id": "5c7e0994-bc22-4190-9774-5f197b1500e6",
            "name": "Test-1",
            "creationTime": "2021-12-03T10:15:30Z",
        },
        "clan": {
            "info": {
                "id": "647d6c53-b3d7-4d30-8d08-de874eb1d845",
                "name": "Clan #1",
                "tag": "TAG",
                "level": 2,
                "levelPoints": 239323,
                "registrationTime": "2022-07-03T10:15:30Z",
                "alliance": "covenant",
                "description": "Sample description",
                "leader": "Test-1",
                "memberCount": 1,
            },
            "member": {"name": "Test-1", "rank": "LEADER", "joinTime": "2022-07-03T10:15:30Z"},
        },
    }


@pytest.fixture
def valid_clan_data() -> TestData:
    return {
        "id": "647d6c53-b3d7-4d30-8d08-de874eb1d845",
        "name": "Clan #1",
        "tag": "TAG",
        "level": 2,
        "levelPoints": 239323,
        "registrationTime": "2022-07-03T10:15:30Z",
        "alliance": "covenant",
        "description": "Sample description",
        "leader": "Test-1",
        "memberCount": 1,
    }


@pytest.fixture
def valid_clan_member_data() -> TestData:
    return {
        "name": "Test-3",
        "rank": "OFFICER",
        "joinTime": "2023-01-03T10:15:30Z",
    }
