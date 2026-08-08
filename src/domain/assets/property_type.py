from datetime import datetime
from enum import Enum, auto


class PropertyType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATETIME = auto()

    def validate(self, value) -> bool | None:
        if self == PropertyType.STRING:
            return type(value) is str

        elif self == PropertyType.INTEGER:
            return type(value) is int

        elif self == PropertyType.FLOAT:
            return type(value) is int or type(value) is float

        elif self == PropertyType.BOOLEAN:
            return type(value) is bool

        elif self == PropertyType.DATETIME:
            return type(value) is datetime
