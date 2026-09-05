from datetime import datetime
from enum import Enum, auto


class PropertyType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATETIME = auto()

    def validate(self, value) -> bool:
        if self == PropertyType.STRING:
            return type(value) is str

        if self == PropertyType.INTEGER:
            return type(value) is int

        if self == PropertyType.FLOAT:
            return type(value) is int or type(value) is float

        if self == PropertyType.BOOLEAN:
            return type(value) is bool

        if self == PropertyType.DATETIME:
            return type(value) is datetime

        return False
