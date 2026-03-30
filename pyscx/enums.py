from enum import StrEnum


class Region(StrEnum):
    """Enumeration of game regions."""

    RU = "ru"
    EU = "eu"
    NA = "na"
    SEA = "sea"
    NEA = "nea"

    def is_motherland(self) -> bool:
        """Check if the region is Russia (motherland).

        Returns:
            bool: True if the region is Russia, False if global (NA, SEA, EU, NEA).
        """
        return self == Region.RU

    def is_global(self) -> bool:
        """Check if the region is global (NA, SEA, EU, NEA).

        Returns:
            bool: True if the region is global, False if Russia.
        """
        return self != Region.RU


# TODO: It may be useless
class Localization(StrEnum):
    """Enumeration of game localizations (languages)."""

    RU = "ru"
    EN = "en"
    ES = "es"
    FR = "fr"
    KO = "ko"


class ColorRank(StrEnum):
    """Enumeration of game color ranks (rarity levels)."""

    DEFAULT = "DEFAULT"  # picklock
    NEWBIE = "RANK_NEWBIE"
    VETERAN = "RANK_VETERAN"
    MASTER = "RANK_MASTER"
    LEGEND = "RANK_LEGEND"


class ItemState(StrEnum):
    """Enumeration of item states (drop possibility)."""

    NONE = "NONE"
    NON_DROP = "NON_DROP"
    PERSONAL_ON_USE = "PERSONAL_ON_USE"
    PERSONAL_ON_GET = "PERSONAL_ON_GET"
    PERSONAL_DROP_ON_GET = "PERSONAL_DROP_ON_GET"  # Barter items


class ItemCategory(StrEnum):
    """Enumeration of item categories.

    Category names are presented in the singular form,
    as this is the category itself. Category values are based
    on the original name from the item database.
    """

    ARMOR = "armor"
    ARTIFACT = "artefact"
    ATTACHMENT = "attachment"
    BACKPACK = "backpacks"
    AMMO = "bullet"
    CONTAINER = "containers"
    DRINK = "drink"
    FOOD = "food"
    GRENADE = "grenade"
    MEDICINE = "medicine"
    MISC = "misc"
    OTHER = "other"
    WEAPON = "weapon"
    WEAPON_MODULE = "weapon_modules"


class ArmorCategory(StrEnum):
    """Enumeration of armor categories."""

    CLOTHES = "clothes"
    COMBAT = "combat"
    COMBINED = "combined"
    DEVICE = "device"
    SCIENTIST = "scientist"


class ArtifactCategory(StrEnum):
    """Enumeration of artifact categories."""

    BIOCHEMICAL = "biochemical"
    ELECTROPHYSICAL = "electrophysical"
    GRAVITY = "gravity"
    THERMAL = "thermal"
    OTHER = "other_arts"


class AttachmentCategory(StrEnum):
    """Enumeration of attachment categories."""

    ACCESSORY = "accessory"
    BARREL = "barrel"
    SIGHT = "collimator_sights"
    FOREND = "forend"
    HANDGRIP = "handgrips"
    MAGAZINE = "mag"
    OTHER = "other"
    PISTOL_GRIP = "pistol_handle"


class OtherCategory(StrEnum):
    """Enumeration of other categories."""

    MOTIF = "armor_motif"
    DEVICE = "device"
    SKIN = "skins"


class WeaponCategory(StrEnum):
    """Enumeration of weapon categories."""

    ASSAULT_RIFLE = "assault_rifle"
    SNIPER_RIFLE = "sniper_rifle"
    SHOTGUN = "shotgun"
    PISTOL = "pistol"
    SUBMACHINE_GUN = "submachine_gun"
    MACHINE_GUN = "machine_gun"
    DEVICE = "device"
    MELEE = "melee"
    HEAVY = "heavy"


class ModuleCategory(StrEnum):
    """Enumeration of weapon module categories."""

    MODULE = "weapon_module"
    CORE = "weapon_module_core"
    REMOVER = "weapon_module_remover"
