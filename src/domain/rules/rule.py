from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .action import Action
from .conditions.condition import Condition
from .exceptions import InvalidRuleDefinitionException
from .trigger import Trigger


@dataclass(frozen=True, eq=True)
class Rule:
    trigger: Trigger
    condition: Condition
    action: Action
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.trigger, Trigger):
            raise InvalidRuleDefinitionException

        if not isinstance(self.condition, Condition):
            raise InvalidRuleDefinitionException

        if not isinstance(self.action, Action):
            raise InvalidRuleDefinitionException

    def __eq__(self, other) -> bool:
        if not isinstance(other, Rule):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
