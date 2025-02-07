class Region(object):
    def __init__(self, id: int = None, name: str = None, *args, **kwargs) -> None:
        # The ability to transfer documents explicitly or as an unpacked dictionary
        for attr, value in {"id": id, "name": name}.items():
            resolved_value = value or kwargs.get(attr)
            setattr(self, attr, resolved_value)

        if None in (self.id, self.name):
            raise ValueError(
                "Both 'id' and 'name' must be provided either explicitly or in kwargs."
            )

    def __repr__(self) -> str:
        return f"Region<id={self.id}>"
