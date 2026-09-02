import pytest

from src.domain.assets.exceptions import InvalidStateTransitionException
from src.domain.assets.state import State
from src.domain.assets.state_transition import StateTransition


def test_can_create_state_transition() -> None:
    active = State("ACTIVE")
    inactive = State("INACTIVE")

    transition = StateTransition(active, inactive)

    assert transition.source == active
    assert transition.target == inactive


def test_state_transition_is_immutable() -> None:
    active = State("ACTIVE")
    inactive = State("INACTIVE")

    transition = StateTransition(active, inactive)

    with pytest.raises(Exception):
        transition.target = active


def test_invalid_source_state_raises() -> None:
    inactive = State("INACTIVE")

    with pytest.raises(InvalidStateTransitionException):
        StateTransition("ACTIVE", inactive)


def test_invalid_target_state_raises() -> None:
    active = State("ACTIVE")

    with pytest.raises(InvalidStateTransitionException):
        StateTransition(active, "INACTIVE")


def test_equivalent_state_transitions_are_equal() -> None:
    active = State("ACTIVE")
    inactive = State("INACTIVE")

    transition_1 = StateTransition(active, inactive)
    transition_2 = StateTransition(active, inactive)

    assert transition_1 == transition_2


def test_transition_direction_matters() -> None:
    active = State("ACTIVE")
    inactive = State("INACTIVE")

    forward = StateTransition(active, inactive)
    reverse = StateTransition(inactive, active)

    assert forward != reverse
