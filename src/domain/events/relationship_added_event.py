from dataclasses import dataclass
from typing import TYPE_CHECKING

from .domain_event import DomainEvent

if TYPE_CHECKING:
    from ..relationships.relationship import Relationship


@dataclass(frozen=True)
class RelationshipAddedEvent(DomainEvent):
    relationship: "Relationship"
