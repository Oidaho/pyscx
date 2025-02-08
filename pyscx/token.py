from enum import Enum


class TokenType(Enum):
    USER = "user"
    APPLICATION = "application"


class Token(object):
    def __init__(self, value: str, type: TokenType) -> None:
        self.value = value
        self.type = type
