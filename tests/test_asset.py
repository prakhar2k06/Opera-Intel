import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.assets.exceptions import (
    InvalidAssetStateTransitionException,
    InvalidPropertyValueException,
    InvalidTargetStateException,
    MissingPropertyException,
    UnknownPropertyException,
    UnpublishedAssetTypeException,
)
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType
from src.domain.assets.state import State
from src.domain.assets.state_transition import StateTransition


def test_cannot_create_asset_from_unpublished_type() -> None:
    asset_type = AssetType("Test")

    with pytest.raises(UnpublishedAssetTypeException):
        Asset("Test_Asset", asset_type, {})


def test_can_create_valid_asset() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    assert asset.name == "Test_Asset"
    assert asset.asset_type is asset_type


def test_asset_stores_supplied_properties() -> None:
    asset_type = AssetType("Test")

    id_property = Property("Id", PropertyType.INTEGER, True, 0)
    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(id_property)
    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Test_Asset",
        asset_type,
        {
            "Id": 10,
            "Count": 5,
        },
    )

    assert asset.properties["Id"] == 10
    assert asset.properties["Count"] == 5


def test_unknown_property_raises() -> None:
    asset_type = AssetType("Test")

    id_property = Property("Id", PropertyType.INTEGER, True, 0)
    asset_type.add_property(id_property)
    asset_type.publish()

    with pytest.raises(UnknownPropertyException):
        Asset(
            "Test_Asset",
            asset_type,
            {
                "Id": 10,
                "fuel": 10,
            },
        )


def test_missing_required_property_raises() -> None:
    asset_type = AssetType("Test")

    required_property = Property(
        "Id",
        PropertyType.INTEGER,
        True,
    )

    asset_type.add_property(required_property)
    asset_type.publish()

    with pytest.raises(MissingPropertyException):
        Asset("Test_Asset", asset_type, {})


def test_invalid_property_type_raises() -> None:
    asset_type = AssetType("Test")

    id_property = Property(
        "Id",
        PropertyType.INTEGER,
        True,
    )

    asset_type.add_property(id_property)
    asset_type.publish()

    with pytest.raises(InvalidPropertyValueException):
        Asset(
            "Test_Asset",
            asset_type,
            {
                "Id": "not-an-integer",
            },
        )


def test_optional_missing_property_defaults_to_none() -> None:
    asset_type = AssetType("Test")

    optional_property = Property(
        "Description",
        PropertyType.STRING,
        False,
    )

    asset_type.add_property(optional_property)
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    assert asset.properties["Description"] is None


def test_missing_property_uses_default_value() -> None:
    asset_type = AssetType("Test")

    count_property = Property(
        "Count",
        PropertyType.INTEGER,
        False,
        0,
    )

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    assert asset.properties["Count"] == 0


def test_supplied_value_overrides_default() -> None:
    asset_type = AssetType("Test")

    count_property = Property(
        "Count",
        PropertyType.INTEGER,
        False,
        0,
    )

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Test_Asset",
        asset_type,
        {
            "Count": 25,
        },
    )

    assert asset.properties["Count"] == 25


def test_required_property_with_default_can_be_omitted() -> None:
    asset_type = AssetType("Test")

    active_property = Property(
        "Active",
        PropertyType.BOOLEAN,
        True,
        True,
    )

    asset_type.add_property(active_property)
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    assert asset.properties["Active"] is True


def test_assets_of_same_type_have_independent_values() -> None:
    asset_type = AssetType("Test")

    count_property = Property(
        "Count",
        PropertyType.INTEGER,
        True,
    )

    asset_type.add_property(count_property)
    asset_type.publish()

    asset_1 = Asset(
        "Asset_1",
        asset_type,
        {"Count": 10},
    )

    asset_2 = Asset(
        "Asset_2",
        asset_type,
        {"Count": 20},
    )

    assert asset_1.properties["Count"] == 10
    assert asset_2.properties["Count"] == 20


def test_asset_current_state_is_initial_state() -> None:
    asset_type = AssetType("Test")
    online = State("ONLINE")

    asset_type.add_state(online)
    asset_type.set_initial_state(online)
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    assert asset.current_state == online


def test_stateless_asset_current_state_is_none() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    assert asset.current_state is None


def test_asset_can_transition() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)

    assert asset.current_state == degraded


def test_asset_can_perform_multiple_valid_transitions() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.add_transition(StateTransition(degraded, offline))

    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)
    asset.transition(offline)

    assert asset.current_state == offline


def test_asset_rejects_non_state_target() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")

    asset_type.add_state(online)
    asset_type.set_initial_state(online)
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    with pytest.raises(InvalidTargetStateException):
        asset.transition([])


def test_asset_rejects_state_not_in_asset_type() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    external_state = State("READY")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    with pytest.raises(InvalidTargetStateException):
        asset.transition(external_state)


def test_asset_rejects_undefined_transition() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)
    asset_type.add_transition(StateTransition(online, degraded))

    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    with pytest.raises(InvalidAssetStateTransitionException):
        asset.transition(offline)


def test_asset_transition_respects_direction() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)

    with pytest.raises(InvalidAssetStateTransitionException):
        asset.transition(online)


def test_update_unknown_property_raises() -> None:
    asset_type = AssetType("Test")

    id_property = Property("Id", PropertyType.INTEGER, True, 0)
    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(id_property)
    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Test_Asset",
        asset_type,
        {
            "Id": 10,
            "Count": 5,
        },
    )
    with pytest.raises(UnknownPropertyException):
        asset.update_property("Fuel", 4)


def test_update_property_with_invalid_value_raises() -> None:
    asset_type = AssetType("Test")

    id_property = Property("Id", PropertyType.INTEGER, True, 0)
    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(id_property)
    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Test_Asset",
        asset_type,
        {
            "Id": 10,
            "Count": 5,
        },
    )
    with pytest.raises(InvalidPropertyValueException):
        asset.update_property("Count", "Wrong")


# -------------------------
# Domain Events
# -------------------------


def test_asset_transition_emits_event() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)

    assert len(asset._domain_events) == 1
    assert asset._domain_events[0].asset is asset
    assert asset._domain_events[0].previous_state == online
    assert asset._domain_events[0].new_state == degraded


def test_failed_asset_transition_emits_no_events() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)
    asset_type.add_transition(StateTransition(online, degraded))

    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    with pytest.raises(InvalidAssetStateTransitionException):
        asset.transition(offline)

    assert len(asset._domain_events) == 0


def test_multiple_transitions_accumulate_events_in_order() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.add_transition(StateTransition(degraded, offline))

    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)
    asset.transition(offline)

    assert len(asset._domain_events) == 2

    assert asset._domain_events[0].previous_state == online
    assert asset._domain_events[0].new_state == degraded

    assert asset._domain_events[1].previous_state == degraded
    assert asset._domain_events[1].new_state == offline


def test_pull_domain_events_returns_and_clears_events() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.add_transition(StateTransition(degraded, offline))

    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    asset.transition(degraded)
    asset.transition(offline)

    events = asset.pull_domain_events()

    assert len(events) == 2
    assert len(asset._domain_events) == 0
    assert asset.pull_domain_events() == []


def test_assets_have_independent_domain_events() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")
    offline = State("OFFLINE")

    for state in (online, degraded, offline):
        asset_type.add_state(state)

    asset_type.set_initial_state(online)

    asset_type.add_transition(StateTransition(online, degraded))
    asset_type.add_transition(StateTransition(degraded, offline))

    asset_type.publish()

    asset_1 = Asset("Asset_1", asset_type, {})
    asset_2 = Asset("Asset_2", asset_type, {})

    asset_1.transition(degraded)
    asset_1.transition(offline)

    asset_2.transition(degraded)

    events_1 = asset_1.pull_domain_events()
    events_2 = asset_2.pull_domain_events()

    assert len(events_1) == 2
    assert len(events_2) == 1

    assert all(event.asset is asset_1 for event in events_1)
    assert all(event.asset is asset_2 for event in events_2)


def test_asset_property_change_emits_event() -> None:
    asset_type = AssetType("Test")

    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Test_Asset",
        asset_type,
        {"Count": 5},
    )

    asset.update_property("Count", 4)

    assert asset.properties["Count"] == 4
    assert len(asset._domain_events) == 1

    event = asset._domain_events[0]

    assert event.asset is asset
    assert event.property == count_property
    assert event.previous_value == 5
    assert event.new_value == 4


def test_updating_property_to_same_value_emits_no_event() -> None:
    asset_type = AssetType("Test")

    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {"Count": 5})

    asset.update_property("Count", 5)

    assert asset.properties["Count"] == 5
    assert asset._domain_events == []


def test_failed_property_update_does_not_change_value_or_emit_event() -> None:
    asset_type = AssetType("Test")

    count_property = Property("Count", PropertyType.INTEGER, True, 0)

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {"Count": 5})

    with pytest.raises(InvalidPropertyValueException):
        asset.update_property("Count", "Wrong")

    assert asset.properties["Count"] == 5
    assert asset._domain_events == []
