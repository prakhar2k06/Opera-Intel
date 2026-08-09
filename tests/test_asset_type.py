import pytest

from src.domain.assets.asset_type import AssetType
from src.domain.assets.exceptions import (
    AssetTypeSchemaLockedException,
    DuplicatePropertyException,
)
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType


def test_asset_type_starts_unpublished() -> None:
    a1 = AssetType("Test")
    assert a1.is_published is False


def test_can_add_property_before_publish() -> None:
    a1 = AssetType("Test")
    p1 = Property("Id", PropertyType.INTEGER, True)
    a1.add_property(p1)


def test_duplicate_property_raises() -> None:
    a1 = AssetType("Test")
    p1 = Property("Id", PropertyType.INTEGER, True)
    a1.add_property(p1)
    p2 = Property("Id", PropertyType.INTEGER, True)

    with pytest.raises(DuplicatePropertyException):
        a1.add_property(p2)


def test_publish_marks_asset_type_as_published() -> None:
    a1 = AssetType("Test")
    a1.publish()
    assert a1.is_published is True


def test_cannot_add_property_after_publish():
    a1 = AssetType("Test")
    a1.publish()
    p1 = Property("Id", PropertyType.INTEGER, True)
    with pytest.raises(AssetTypeSchemaLockedException):
        a1.add_property(p1)
