import pytest

from src.domain.assets.exceptions import InvalidStateDefinitionException
from src.domain.assets.state import State


def test_can_create_state() -> None:
    state = State("ACTIVE")

    assert state.name == "ACTIVE"


def test_state_is_immutable() -> None:
    state = State("ACTIVE")

    with pytest.raises(Exception):
        state.name = "INACTIVE"


def test_empty_state_name_raises() -> None:
    with pytest.raises(InvalidStateDefinitionException):
        State("")


def test_whitespace_state_name_raises() -> None:
    with pytest.raises(InvalidStateDefinitionException):
        State("   ")


def test_non_string_state_name_raises() -> None:
    with pytest.raises(InvalidStateDefinitionException):
        State(123)


def test_states_with_same_name_are_equal() -> None:
    assert State("ACTIVE") == State("ACTIVE")
