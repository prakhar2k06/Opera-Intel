from dataclasses import dataclass

from ...assets.asset import Asset
from ...assets.property import Property
from ..exceptions import InvalidConditionDefinitionException
from .condition import Condition


@dataclass(frozen=True)
class AndCondition(Condition):
    condition_1: Condition
    condition_2: Condition

    def __post_init__(self) -> None:
        if not isinstance(self.condition_1, Condition):
            raise InvalidConditionDefinitionException

        if not isinstance(self.condition_2, Condition):
            raise InvalidConditionDefinitionException

    def evaluate(self, asset: Asset) -> bool:
        return self.condition_1.evaluate(asset) and self.condition_2.evaluate(asset)

    def get_referenced_properties(self) -> set[Property]:
        return (
            self.condition_1.get_referenced_properties()
            | self.condition_2.get_referenced_properties()
        )
