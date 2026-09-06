from dataclasses import dataclass

from ..events.domain_event import DomainEvent
from .exceptions import InvalidTriggerDefinitionException


@dataclass(frozen=True)
class Trigger:
    trigger_event: type[DomainEvent]

    def __post_init__(self) -> None:
        if (
            not self.trigger_event
            or not isinstance(self.trigger_event, type)
            or not issubclass(self.trigger_event, DomainEvent)
        ):
            raise InvalidTriggerDefinitionException
