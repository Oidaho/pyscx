from collections.abc import Mapping

from pydantic import AliasPath, BaseModel, Field, model_validator

from pyscx.enums import (
    ArmorCategory,
    ArtifactCategory,
    AttachmentCategory,
    ColorRank,
    ItemState,
    ModuleCategory,
    OtherCategory,
    WeaponCategory,
)
from pyscx.enums import ItemCategory as ItemCategory_
from pyscx.models import StalcraftEntity

type Subcategory = (
    ArmorCategory
    | ArtifactCategory
    | AttachmentCategory
    | OtherCategory
    | WeaponCategory
    | ModuleCategory
)


SUBCATEGORY_MAP: Mapping[ItemCategory_, type[Subcategory]] = {
    ItemCategory_.OTHER: OtherCategory,
    ItemCategory_.WEAPON: WeaponCategory,
    ItemCategory_.WEAPON_MODULE: ModuleCategory,
    ItemCategory_.ARTIFACT: ArtifactCategory,
    ItemCategory_.ATTACHMENT: AttachmentCategory,
    ItemCategory_.ARMOR: ArmorCategory,
}


class ItemNameTranslation(BaseModel):
    """Represents the translations for an item's name."""

    ru: str
    en: str
    es: str
    fr: str
    ko: str


class ItemName(BaseModel):
    """Represents the name of an item, including its key and translations."""

    key: str = Field(validation_alias=AliasPath("key"))
    translation: ItemNameTranslation = Field(validation_alias=AliasPath("lines"))


class ItemCategory(BaseModel):
    """Represents the category of an item."""

    name: ItemCategory_
    subcategory: Subcategory | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_category(cls, data: str) -> dict[str, str | None]:
        """Validate and parse the 'category' field from the input data."""

        category, subcategory = data.split("/", 1) if "/" in data else (data, None)

        if subcategory and (subcat_enum := SUBCATEGORY_MAP.get(ItemCategory_(category))):
            # Protection against invalid subcategory names
            # and ensuring that the subcategory name belongs to the
            # correct subcategory type.
            subcategory = subcat_enum(subcategory) if subcategory in subcat_enum else None

        return {"name": category, "subcategory": subcategory}


class GameItem(StalcraftEntity):
    """Base game item model."""

    id: str
    category: ItemCategory
    name: ItemName
    color: ColorRank
    status: ItemState = Field(validation_alias=AliasPath("status", "state"))
