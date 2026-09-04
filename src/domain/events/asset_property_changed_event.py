from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..assets.property import Property
from .domain_event import DomainEvent

if TYPE_CHECKING:
    from ..assets.asset import Asset


@dataclass(frozen=True)
class AssetPropertyChangedEvent(DomainEvent):
    asset: "Asset"
    property: Property
    previous_value: object
    new_value: object
