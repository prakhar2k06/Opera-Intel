from dataclasses import dataclass

from .exceptions import InvalidStateTransitionException
from .state import State


@dataclass(frozen=True)
class StateTransition:
    source: State
    target: State

    def __post_init__(self) -> None:
        if not isinstance(self.source, State) or not isinstance(self.target, State):
            raise InvalidStateTransitionException
