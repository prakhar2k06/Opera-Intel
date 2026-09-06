from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ...assets.property import Property

if TYPE_CHECKING:
    from ...assets.asset import Asset


class Condition(ABC):
    @abstractmethod
    def evaluate(self, asset: "Asset") -> bool:
        pass

    @abstractmethod
    def get_referenced_properties(self) -> set[Property]:
        pass
