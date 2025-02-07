class StalcraftObject(object):
    def raw(self) -> dict[str, any]:
        return {key: value for key, value in vars(self).items()}
