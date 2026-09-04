from dataclasses import FrozenInstanceError
from datetime import timezone

import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType
from src.domain.assets.state import State
from src.domain.events.asset_property_changed_event import AssetPropertyChangedEvent
from src.domain.events.asset_state_changed_event import AssetStateChangedEvent
from src.domain.events.domain_event import DomainEvent

# -------------------------
# DomainEvent
# -------------------------


def test_domain_event_gets_timestamp() -> None:
    event = DomainEvent()

    assert event.occurred_at is not None


def test_domain_event_timestamp_is_utc() -> None:
    event = DomainEvent()

    assert event.occurred_at.tzinfo is not None
    assert event.occurred_at.utcoffset() == timezone.utc.utcoffset(event.occurred_at)


def test_domain_event_is_immutable() -> None:
    event = DomainEvent()

    with pytest.raises(FrozenInstanceError):
        event.occurred_at = event.occurred_at


# -------------------------
# AssetStateChangedEvent
# -------------------------


def test_asset_state_changed_event_stores_values() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    event = AssetStateChangedEvent(
        asset=asset,
        previous_state=online,
        new_state=degraded,
    )

    assert event.asset is asset
    assert event.previous_state == online
    assert event.new_state == degraded
    assert event.occurred_at is not None


def test_asset_state_changed_event_is_immutable() -> None:
    asset_type = AssetType("Test")

    online = State("ONLINE")
    degraded = State("DEGRADED")

    asset_type.add_state(online)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(online)
    asset_type.publish()

    asset = Asset("Asset_1", asset_type, {})

    event = AssetStateChangedEvent(
        asset=asset,
        previous_state=online,
        new_state=degraded,
    )

    with pytest.raises(FrozenInstanceError):
        event.new_state = online


# -------------------------
# AssetPropertyChangedEvent
# -------------------------


def test_asset_property_changed_event_stores_values() -> None:
    asset_type = AssetType("Test")

    count_property = Property(
        "Count",
        PropertyType.INTEGER,
        True,
    )

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Count": 5},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=count_property,
        previous_value=5,
        new_value=10,
    )

    assert event.asset is asset
    assert event.property == count_property
    assert event.previous_value == 5
    assert event.new_value == 10
    assert event.occurred_at is not None


def test_asset_property_changed_event_is_immutable() -> None:
    asset_type = AssetType("Test")

    count_property = Property(
        "Count",
        PropertyType.INTEGER,
        True,
    )

    asset_type.add_property(count_property)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Count": 5},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=count_property,
        previous_value=5,
        new_value=10,
    )

    with pytest.raises(FrozenInstanceError):
        event.new_value = 20
