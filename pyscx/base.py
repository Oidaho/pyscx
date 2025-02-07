class StalcraftObject(object):
    def raw(self) -> dict[str, any]:
        return self.__dict__
