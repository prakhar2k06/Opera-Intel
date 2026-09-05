from enum import Enum, auto

from ...assets.property_type import PropertyType


class Comparison(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()

    GREATER_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN = auto()
    LESS_THAN_OR_EQUAL = auto()

    CONTAINS = auto()
    STARTS_WITH = auto()
    ENDS_WITH = auto()

    def evaluate(self, left, right) -> bool:
        if self == Comparison.EQUAL:
            return left == right

        if self == Comparison.NOT_EQUAL:
            return left != right

        if self == Comparison.GREATER_THAN:
            return left > right

        if self == Comparison.GREATER_THAN_OR_EQUAL:
            return left >= right

        if self == Comparison.LESS_THAN:
            return left < right

        if self == Comparison.LESS_THAN_OR_EQUAL:
            return left <= right

        if self == Comparison.CONTAINS:
            return right in left

        if self == Comparison.STARTS_WITH:
            return left.startswith(right)

        if self == Comparison.ENDS_WITH:
            return left.endswith(right)

        return False

    def supports_property_type(self, property_type: PropertyType) -> bool:
        if not isinstance(property_type, PropertyType):
            return False

        if property_type == PropertyType.STRING:
            return self in (
                Comparison.EQUAL,
                Comparison.NOT_EQUAL,
                Comparison.CONTAINS,
                Comparison.STARTS_WITH,
                Comparison.ENDS_WITH,
            )

        if property_type in (
            PropertyType.INTEGER,
            PropertyType.FLOAT,
            PropertyType.DATETIME,
        ):
            return self in (
                Comparison.EQUAL,
                Comparison.NOT_EQUAL,
                Comparison.GREATER_THAN,
                Comparison.GREATER_THAN_OR_EQUAL,
                Comparison.LESS_THAN,
                Comparison.LESS_THAN_OR_EQUAL,
            )

        if property_type == PropertyType.BOOLEAN:
            return self in (
                Comparison.EQUAL,
                Comparison.NOT_EQUAL,
            )

        return False
