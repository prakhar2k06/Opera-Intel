from dataclasses import dataclass

from ..assets.state import State
from .exceptions import InvalidActionDefinitionException


@dataclass(frozen=True)
class Action:
    transition_to: State

    def __post_init__(self) -> None:
        if not isinstance(self.transition_to, State):
            raise InvalidActionDefinitionException
