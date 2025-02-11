from typing import Any

import pytest


TestData = dict[str, Any] | list[dict[str, Any]] | list[Any]


@pytest.fixture
def valid_region_list() -> TestData:
    return [
        {"id": "RU", "name": "RUSSIA"},
        {"id": "EU", "name": "EUROPE"},
        {"id": "NA", "name": "NORTH AMERICA"},
        {"id": "SEA", "name": "SOUTH EAST ASIA"},
    ]


@pytest.fixture
def valid_emission_information_data() -> TestData:
    return {
        "currentStart": "2019-08-24T14:15:22Z",
        "previousStart": "2019-08-24T14:15:22Z",
        "previousEnd": "2019-08-24T14:15:22Z",
    }


@pytest.fixture
def valid_freind_list() -> TestData:
    return ["Test-2", "Test-3"]


@pytest.fixture
def valid_price_history_data() -> TestData:
    return [
        {"amount": 1, "price": 1000, "time": "2025-02-11T02:48:47.001594Z", "additional": {}},
        {"amount": 2, "price": 2000, "time": "2025-02-11T02:33:47.001597Z", "additional": {}},
        {"amount": 3, "price": 3000, "time": "2025-02-11T02:18:47.001598Z", "additional": {}},
        {"amount": 4, "price": 4000, "time": "2025-02-11T02:03:47.001599Z", "additional": {}},
        {"amount": 1, "price": 0, "time": "2025-02-11T01:48:47.001599Z", "additional": {}},
        {"amount": 2, "price": 1000, "time": "2025-02-11T01:33:47.001599Z", "additional": {}},
        {"amount": 3, "price": 2000, "time": "2025-02-11T01:18:47.001600Z", "additional": {}},
        {"amount": 4, "price": 3000, "time": "2025-02-11T01:03:47.001600Z", "additional": {}},
        {"amount": 1, "price": 4000, "time": "2025-02-11T00:48:47.001601Z", "additional": {}},
        {"amount": 2, "price": 0, "time": "2025-02-11T00:33:47.001601Z", "additional": {}},
    ]


@pytest.fixture
def valid_active_lots_data() -> TestData:
    return [
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-11T00:49:55.603680Z",
            "endTime": "2025-02-11T12:49:55.603683Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-10T00:49:55.603687Z",
            "endTime": "2025-02-11T12:49:55.603687Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-09T00:49:55.603688Z",
            "endTime": "2025-02-11T12:49:55.603688Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-08T00:49:55.603689Z",
            "endTime": "2025-02-11T12:49:55.603689Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-07T00:49:55.603690Z",
            "endTime": "2025-02-11T12:49:55.603690Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-06T00:49:55.603691Z",
            "endTime": "2025-02-11T12:49:55.603691Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-05T00:49:55.603692Z",
            "endTime": "2025-02-11T12:49:55.603692Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-04T00:49:55.603693Z",
            "endTime": "2025-02-11T12:49:55.603693Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-03T00:49:55.603694Z",
            "endTime": "2025-02-11T12:49:55.603694Z",
            "additional": {},
        },
        {
            "itemId": "1kv2",
            "amount": 1,
            "startPrice": 100,
            "buyoutPrice": 10000,
            "startTime": "2025-02-02T00:49:55.603695Z",
            "endTime": "2025-02-11T12:49:55.603695Z",
            "additional": {},
        },
    ]


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
def valid_user_characters_list() -> TestData:
    return [
        {
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
        },
        {
            "information": {
                "id": "996e2cf9-5f36-4a38-97e8-1aecec42b5f0",
                "name": "Test-2",
                "creationTime": "2022-12-03T10:15:30Z",
            },
            "clan": {
                "info": {
                    "id": "a5a7f97f-5725-4b84-85c2-fffb15feea39",
                    "name": "Clan #2",
                    "tag": "TBA",
                    "level": 1,
                    "levelPoints": 3732342,
                    "registrationTime": "2022-12-13T10:15:30Z",
                    "alliance": "duty",
                    "description": "Sample description",
                    "leader": "Test-2",
                    "memberCount": 2,
                },
                "member": {"name": "Test-2", "rank": "LEADER", "joinTime": "2022-12-13T10:15:30Z"},
            },
        },
        {
            "information": {
                "id": "9219dfbb-1332-4dc7-b3be-fc4b089710cb",
                "name": "Test-3",
                "creationTime": "2023-01-03T10:15:30Z",
            },
            "clan": {
                "info": {
                    "id": "a5a7f97f-5725-4b84-85c2-fffb15feea39",
                    "name": "Clan #2",
                    "tag": "TBA",
                    "level": 1,
                    "levelPoints": 3732342,
                    "registrationTime": "2022-12-13T10:15:30Z",
                    "alliance": "duty",
                    "description": "Sample description",
                    "leader": "Test-2",
                    "memberCount": 2,
                },
                "member": {"name": "Test-3", "rank": "OFFICER", "joinTime": "2023-01-03T10:15:30Z"},
            },
        },
    ]


@pytest.fixture
def valid_clan_list() -> TestData:
    return [
        {
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
        {
            "id": "a5a7f97f-5725-4b84-85c2-fffb15feea39",
            "name": "Clan #2",
            "tag": "TBA",
            "level": 1,
            "levelPoints": 3732342,
            "registrationTime": "2022-12-13T10:15:30Z",
            "alliance": "duty",
            "description": "Sample description",
            "leader": "Test-2",
            "memberCount": 2,
        },
    ]


@pytest.fixture
def valid_clan_information_data() -> TestData:
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
def valid_clan_members_list() -> TestData:
    return [
        {"name": "Test-2", "rank": "LEADER", "joinTime": "2022-12-13T10:15:30Z"},
        {"name": "Test-3", "rank": "OFFICER", "joinTime": "2023-01-03T10:15:30Z"},
    ]
