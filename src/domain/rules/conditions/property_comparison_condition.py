from dataclasses import dataclass

from ...assets.asset import Asset
from ...assets.property import Property
from ..exceptions import InvalidConditionDefinitionException
from .comparison import Comparison
from .condition import Condition


@dataclass(frozen=True)
class PropertyComparisonCondition(Condition):
    property: Property
    comparison: Comparison
    value: object

    def __post_init__(self) -> None:
        if not isinstance(self.property, Property):
            raise InvalidConditionDefinitionException

        if not isinstance(self.comparison, Comparison):
            raise InvalidConditionDefinitionException

        if not self.comparison.supports_property_type(self.property.property_type):
            raise InvalidConditionDefinitionException

        if not self.property.property_type.validate(self.value):
            raise InvalidConditionDefinitionException

    def evaluate(self, asset: Asset) -> bool:
        current_value = asset.properties[self.property.name]

        return self.comparison.evaluate(
            current_value,
            self.value,
        )

    def get_referenced_properties(self) -> set[Property]:
        return {self.property}
