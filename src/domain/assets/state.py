from dataclasses import dataclass

from .exceptions import InvalidStateDefinitionException


@dataclass(frozen=True)
class State:
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise InvalidStateDefinitionException
