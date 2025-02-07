class Region(object):
    def __init__(self, id: int = None, name: str = None, *args, **kwargs) -> None:
        # The ability to transfer documents explicitly or as an unpacked dictionary
        self.id = id if id is not None else kwargs.get("id")
        self.name = name if name is not None else kwargs.get("name")

        if self.id is None or self.name is None:
            raise ValueError(
                "Both 'id' and 'name' must be provided either explicitly or in kwargs."
            )

    def __repr__(self) -> str:
        return f"Region<name={self.name}>"
