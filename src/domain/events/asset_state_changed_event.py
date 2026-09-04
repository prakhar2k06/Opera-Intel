from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..assets.state import State
from .domain_event import DomainEvent

if TYPE_CHECKING:
    from ..assets.asset import Asset


@dataclass(frozen=True)
class AssetStateChangedEvent(DomainEvent):
    asset: "Asset"
    previous_state: State
    new_state: State
