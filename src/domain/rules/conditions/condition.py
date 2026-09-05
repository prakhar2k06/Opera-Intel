from abc import ABC, abstractmethod

from ...assets.asset import Asset
from ...assets.property import Property


class Condition(ABC):
    @abstractmethod
    def evaluate(self, asset: Asset) -> bool:
        pass

    @abstractmethod
    def get_referenced_properties(self) -> set[Property]:
        pass
