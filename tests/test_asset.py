import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.assets.exceptions import (
    InvalidPropertyValueException,
    MissingPropertyException,
    UnknownPropertyException,
    UnpublishedAssetTypeException,
)
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType


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
