from dataclasses import dataclass

from ..events.domain_event import DomainEvent
from .exceptions import InvalidTriggerDefinitionException


@dataclass(frozen=True)
class Trigger:
    trigger_event: DomainEvent

    def __post_init__(self) -> None:
        if not self.trigger_event or not issubclass(self.trigger_event, DomainEvent):
            raise InvalidTriggerDefinitionException
