from .nodes import Node, GetterNode, VariantsGetterNode


class Armor(Node):
    """Represents a category of armor and provides access to its respective data."""

    @property
    def clothes(self) -> VariantsGetterNode:
        """Provides access to clothes armor data."""
        return self._child(VariantsGetterNode, resource="clothes")

    @property
    def combat(self) -> VariantsGetterNode:
        """Provides access to combat armor data."""
        return self._child(VariantsGetterNode, resource="combat")

    @property
    def combined(self) -> VariantsGetterNode:
        """Provides access to combined armor data."""
        return self._child(VariantsGetterNode, resource="combined")

    @property
    def scientists(self) -> VariantsGetterNode:
        """Provides access to scientists armor data."""
        return self._child(VariantsGetterNode, resource="device")

    @property
    def devices(self) -> GetterNode:
        """Provides access to device data."""
        return self._child(GetterNode, resource="device")


class Artifacts(Node):
    """Represents a category of artifacts and provides access to its respective data."""

    @property
    def biochemical(self) -> VariantsGetterNode:
        """Provides access to biochemical artifacts data."""
        return self._child(VariantsGetterNode, resource="biochemical")

    @property
    def electrophysical(self) -> VariantsGetterNode:
        """Provides access to electrophysical artifacts data."""
        return self._child(VariantsGetterNode, resource="electrophysical")

    @property
    def gravity(self) -> VariantsGetterNode:
        """Provides access to gravity artifacts data."""
        return self._child(VariantsGetterNode, resource="gravity")

    @property
    def thermal(self) -> VariantsGetterNode:
        """Provides access to thermal artifacts data."""
        return self._child(VariantsGetterNode, resource="thermal")

    @property
    def other(self) -> VariantsGetterNode:
        """Provides access to other artifacts data."""
        return self._child(VariantsGetterNode, resource="other_arts")


class Attachments(Node):
    """Represents a category of weapon attachments (modifications) and provides
    access to its respective data.
    """

    @property
    def accessories(self) -> GetterNode:
        """Provides access to accessories data."""
        return self._child(GetterNode, resource="accessory")

    @property
    def barrels(self) -> GetterNode:
        """Provides access to barrels data."""
        return self._child(GetterNode, resource="barrel")

    @property
    def sights(self) -> GetterNode:
        """Provides access to sights data."""
        return self._child(GetterNode, resource="collimator_sights")

    @property
    def forends(self) -> GetterNode:
        """Provides access to forends data."""
        return self._child(GetterNode, resource="forend")

    @property
    def handgrips(self) -> GetterNode:
        """Provides access to handgrips data."""
        return self._child(GetterNode, resource="handgrips")

    @property
    def magazines(self) -> GetterNode:
        """Provides access to magazines data."""
        return self._child(GetterNode, resource="mag")

    @property
    def pistol_grips(self) -> GetterNode:
        """Provides access to pistol grips data."""
        return self._child(GetterNode, resource="pistol_handle")

    @property
    def other(self) -> GetterNode:
        """Provides access to other attachments data."""
        return self._child(GetterNode, resource="other")


class Other(GetterNode):
    """Represents a category of other assets and provides access to its respective data."""

    @property
    def devices(self) -> GetterNode:
        """Provides access to devices data."""
        return self._child(GetterNode, resource="device")

    @property
    def skins(self) -> GetterNode:
        """Provides access to skins data."""
        return self._child(GetterNode, resource="skins")


class Weapons(Node):
    """Represents a category of weapons and provides access to its respective data."""

    @property
    def pistols(self) -> VariantsGetterNode:
        """Provides access to pistols data."""
        return self._child(VariantsGetterNode, resource="pistol")

    @property
    def shotguns(self) -> VariantsGetterNode:
        """Provides access to shotguns data."""
        return self._child(VariantsGetterNode, resource="shotgun_rifle")

    @property
    def machine_guns(self) -> VariantsGetterNode:
        """Provides access to machine guns data."""
        return self._child(VariantsGetterNode, resource="machine_gun")

    @property
    def submachine_guns(self) -> VariantsGetterNode:
        """Provides access to submachine guns data."""
        return self._child(VariantsGetterNode, resource="submachine_gun")

    @property
    def assault_rifles(self) -> VariantsGetterNode:
        """Provides access to assault rifles data."""
        return self._child(VariantsGetterNode, resource="assault_rifle")

    @property
    def sniper_rifles(self) -> VariantsGetterNode:
        """Provides access to sniper rifles data."""
        return self._child(VariantsGetterNode, resource="sniper_rifle")

    @property
    def heavy(self) -> VariantsGetterNode:
        """Provides access to heavy weapons data."""
        return self._child(VariantsGetterNode, resource="heavy")

    @property
    def melee(self) -> GetterNode:
        """Provides access to melee weapons data."""
        return self._child(GetterNode, resource="melee")

    @property
    def devices(self) -> VariantsGetterNode:
        """Provides access to devices data."""
        return self._child(VariantsGetterNode, resource="device")


class Modules(Node):
    """Represents a category of weapon modules and provides access to its respective data."""

    @property
    def module(self) -> GetterNode:
        """Provides access to weapon modules data."""
        return self._child(GetterNode, resource="weapon_module")

    @property
    def module_core(self) -> GetterNode:
        """Provides access to weapon module cores data."""
        return self._child(GetterNode, resource="weapon_module_core")

    @property
    def module_remover(self) -> GetterNode:
        """Provides access to weapon module removers data."""
        return self._child(GetterNode, resource="weapon_module_remover")


class Assets(Node):
    """Represents a category of assets and provides access to its respective data."""

    @property
    def armor(self) -> Armor:
        """Provides access to armor category."""
        return self._child(Armor, resource="armor")

    @property
    def artifacts(self) -> Artifacts:
        """Provides access to artifacts category."""
        return self._child(Artifacts, resource="artefact")

    @property
    def attachments(self) -> Attachments:
        """Provides access to attachments category."""
        return self._child(Attachments, resource="attachment")

    @property
    def backpacks(self) -> GetterNode:
        """Provides access to backpacks category."""
        return self._child(GetterNode, resource="backpacks")

    @property
    def ammo(self) -> GetterNode:
        """Provides access to ammo category."""
        return self._child(GetterNode, resource="bullet")

    @property
    def containers(self) -> GetterNode:
        """Provides access to containers category."""
        return self._child(GetterNode, resource="containers")

    @property
    def drinks(self) -> GetterNode:
        """Provides access to drinks category."""
        return self._child(GetterNode, resource="drink")

    @property
    def food(self) -> GetterNode:
        """Provides access to food category."""
        return self._child(GetterNode, resource="food")

    @property
    def grenades(self) -> GetterNode:
        """Provides access to grenades category."""
        return self._child(GetterNode, resource="grenade")

    @property
    def medicine(self) -> GetterNode:
        """Provides access to medicine category."""
        return self._child(GetterNode, resource="medicine")

    @property
    def misc(self) -> GetterNode:
        """Provides access to misc category."""
        return self._child(GetterNode, resource="misc")

    @property
    def other(self) -> Other:
        """Provides access to other category."""
        return self._child(Other, resource="other")

    @property
    def weapons(self) -> Weapons:
        """Provides access to weapons category."""
        return self._child(Weapons, resource="weapon")

    @property
    def modules(self) -> Modules:
        """Provides access to weapon modules category."""
        return self._child(Modules, resource="weapon_modules")


class Region(Node):
    """Represents a game region and provides access to its respective data categories."""

    @property
    def icons(self) -> Assets:
        """Provides access to game icons category."""
        return self._child(Assets, resource="icons", extension=".png")

    @property
    def items(self) -> Assets:
        """Provides access to game items category."""
        return self._child(Assets, resource="items", extension=".json")

    # TODO: This methods means large files download. Think about better way to implement them.
    def achievements(self) -> None: ...
    def barter_recipes(self) -> None: ...
    def hideout_recipes(self) -> None: ...
    def listing(self) -> None: ...
    def stats(self) -> None: ...
