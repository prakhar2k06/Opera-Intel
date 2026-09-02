import pytest

from src.domain.assets.asset_type import AssetType
from src.domain.assets.exceptions import (
    AssetTypeSchemaLockedException,
    DuplicatePropertyException,
    DuplicateStateException,
    DuplicateTransitionException,
    InitialStateNotSetException,
    InvalidStateDefinitionException,
    InvalidStateTransitionException,
    StateNotInAssetTypeException,
)
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType
from src.domain.assets.state import State
from src.domain.assets.state_transition import StateTransition


def test_asset_type_starts_unpublished() -> None:
    asset_type = AssetType("Test")

    assert asset_type.is_published is False


def test_can_add_property_before_publish() -> None:
    asset_type = AssetType("Test")
    property = Property("Id", PropertyType.INTEGER, True)

    asset_type.add_property(property)

    assert asset_type.properties["Id"] == property


def test_duplicate_property_raises() -> None:
    asset_type = AssetType("Test")

    property_1 = Property("Id", PropertyType.INTEGER, True)
    property_2 = Property("Id", PropertyType.INTEGER, True)

    asset_type.add_property(property_1)

    with pytest.raises(DuplicatePropertyException):
        asset_type.add_property(property_2)


def test_publish_marks_asset_type_as_published() -> None:
    asset_type = AssetType("Test")

    asset_type.publish()

    assert asset_type.is_published is True


def test_stateless_asset_type_can_be_published() -> None:
    asset_type = AssetType("Test")

    asset_type.publish()

    assert asset_type.is_published is True


def test_cannot_add_property_after_publish() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    property = Property("Id", PropertyType.INTEGER, True)

    with pytest.raises(AssetTypeSchemaLockedException):
        asset_type.add_property(property)


def test_can_add_state_before_publish() -> None:
    asset_type = AssetType("Test")
    state = State("ACTIVE")

    asset_type.add_state(state)

    assert state in asset_type.states


def test_duplicate_state_raises() -> None:
    asset_type = AssetType("Test")
    state = State("ACTIVE")

    asset_type.add_state(state)

    with pytest.raises(DuplicateStateException):
        asset_type.add_state(state)


def test_invalid_state_type_raises() -> None:
    asset_type = AssetType("Test")

    with pytest.raises(InvalidStateDefinitionException):
        asset_type.add_state("ACTIVE")


def test_cannot_add_state_after_publish() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    state = State("ACTIVE")

    with pytest.raises(AssetTypeSchemaLockedException):
        asset_type.add_state(state)


def test_can_set_initial_state() -> None:
    asset_type = AssetType("Test")
    state = State("ACTIVE")

    asset_type.add_state(state)
    asset_type.set_initial_state(state)

    assert asset_type.initial_state == state


def test_initial_state_can_be_changed_before_publish() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    asset_type.set_initial_state(active)
    asset_type.set_initial_state(inactive)

    assert asset_type.initial_state == inactive


def test_initial_state_must_belong_to_asset_type() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    unknown = State("UNKNOWN")

    asset_type.add_state(active)

    with pytest.raises(StateNotInAssetTypeException):
        asset_type.set_initial_state(unknown)


def test_invalid_initial_state_type_raises() -> None:
    asset_type = AssetType("Test")

    with pytest.raises(InvalidStateDefinitionException):
        asset_type.set_initial_state("ACTIVE")


def test_cannot_set_initial_state_after_publish() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)
    asset_type.set_initial_state(active)
    asset_type.publish()

    with pytest.raises(AssetTypeSchemaLockedException):
        asset_type.set_initial_state(inactive)


def test_stateful_asset_type_requires_initial_state_before_publish() -> None:
    asset_type = AssetType("Test")

    asset_type.add_state(State("ACTIVE"))

    with pytest.raises(InitialStateNotSetException):
        asset_type.publish()


def test_stateful_asset_type_can_publish_with_initial_state() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")

    asset_type.add_state(active)
    asset_type.set_initial_state(active)

    asset_type.publish()

    assert asset_type.is_published is True


def test_can_add_transition() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    transition = StateTransition(active, inactive)

    asset_type.add_transition(transition)

    assert transition in asset_type.transitions


def test_duplicate_transition_raises() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    transition = StateTransition(active, inactive)

    asset_type.add_transition(transition)

    with pytest.raises(DuplicateTransitionException):
        asset_type.add_transition(transition)


def test_invalid_transition_type_raises() -> None:
    asset_type = AssetType("Test")

    with pytest.raises(InvalidStateTransitionException):
        asset_type.add_transition("ACTIVE_TO_INACTIVE")


def test_transition_source_must_belong_to_asset_type() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(inactive)

    transition = StateTransition(active, inactive)

    with pytest.raises(StateNotInAssetTypeException):
        asset_type.add_transition(transition)


def test_transition_target_must_belong_to_asset_type() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)

    transition = StateTransition(active, inactive)

    with pytest.raises(StateNotInAssetTypeException):
        asset_type.add_transition(transition)


def test_cannot_add_transition_after_publish() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)
    asset_type.set_initial_state(active)

    asset_type.publish()

    transition = StateTransition(active, inactive)

    with pytest.raises(AssetTypeSchemaLockedException):
        asset_type.add_transition(transition)


def test_can_transition_returns_true_for_defined_transition() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    asset_type.add_transition(StateTransition(active, inactive))

    assert asset_type.can_transition(active, inactive) is True


def test_can_transition_returns_false_for_undefined_transition() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    assert asset_type.can_transition(active, inactive) is False


def test_can_transition_respects_direction() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)
    asset_type.add_state(inactive)

    asset_type.add_transition(StateTransition(active, inactive))

    assert asset_type.can_transition(active, inactive) is True
    assert asset_type.can_transition(inactive, active) is False


def test_can_transition_rejects_unknown_source_state() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(inactive)

    with pytest.raises(StateNotInAssetTypeException):
        asset_type.can_transition(active, inactive)


def test_can_transition_rejects_unknown_target_state() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    inactive = State("INACTIVE")

    asset_type.add_state(active)

    with pytest.raises(StateNotInAssetTypeException):
        asset_type.can_transition(active, inactive)


def test_can_transition_rejects_invalid_state_type() -> None:
    asset_type = AssetType("Test")

    active = State("ACTIVE")
    asset_type.add_state(active)

    with pytest.raises(InvalidStateDefinitionException):
        asset_type.can_transition(active, "INACTIVE")
