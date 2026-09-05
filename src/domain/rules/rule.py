from dataclasses import dataclass

from .action import Action
from .conditions.condition import Condition
from .exceptions import InvalidRuleDefinitionException
from .trigger import Trigger


@dataclass(frozen=True)
class Rule:
    trigger: Trigger
    condition: Condition
    action: Action

    def __post_init__(self) -> None:
        if not isinstance(self.trigger, Trigger):
            raise InvalidRuleDefinitionException

        if not isinstance(self.condition, Condition):
            raise InvalidRuleDefinitionException

        if not isinstance(self.action, Action):
            raise InvalidRuleDefinitionException
