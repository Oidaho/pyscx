import pytest

from pyscx.objects import (
    APIObject,
    AuctionLot,
    AuctionRedeemedLot,
    CharacterInfo,
    Clan,
    ClanMember,
    Emission,
    FullCharacterInfo,
    Region,
)


@pytest.mark.parametrize(
    "model, fixture_name",
    [
        pytest.param(Emission, "valid_emission_data", id="Emission"),
        pytest.param(Region, "valid_region_data", id="Region"),
        pytest.param(AuctionLot, "valid_active_lot_data", id="AuctionLot"),
        pytest.param(AuctionRedeemedLot, "valid_redeemed_lot_data", id="AuctionRedeemedLot"),
        pytest.param(CharacterInfo, "valid_user_character_data", id="CharacterInfo"),
        pytest.param(FullCharacterInfo, "valid_character_profile_data", id="FullCharacterInfo"),
        pytest.param(Clan, "valid_clan_data", id="Clan"),
        pytest.param(ClanMember, "valid_clan_member_data", id="ClanMember"),
    ],
)
def test_model_creation(model: APIObject, fixture_name: str, request: pytest.FixtureRequest):
    """Checking the correctness of parsing raw data from the API response."""
    data = request.getfixturevalue(fixture_name)
    lot = model(**data)
    assert lot.raw() == data, f"The {model.__name__} object incorrectly parses raw data."
