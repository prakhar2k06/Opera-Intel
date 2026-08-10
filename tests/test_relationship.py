import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.relationships.exceptions import (
    InvalidRelationshipAssetException,
    InvalidRelationshipTypeException,
    RelationshipTypeMismatchException,
)
from src.domain.relationships.relationship import Relationship
from src.domain.relationships.relationship_type import RelationshipType


def test_can_create_valid_relationship() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    relation = Relationship(relation_type, a1, a2)


def test_wrong_source_asset_type_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(RelationshipTypeMismatchException):
        relation = Relationship(relation_type, a2, a2)


def test_wrong_target_asset_type_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(RelationshipTypeMismatchException):
        relation = Relationship(relation_type, a1, a1)


def test_reversed_source_and_target_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(RelationshipTypeMismatchException):
        relation = Relationship(relation_type, a2, a1)


def test_invalid_relationship_type_object_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    with pytest.raises(InvalidRelationshipTypeException):
        relation = Relationship([], a2, a1)


def test_invalid_source_asset_object_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(InvalidRelationshipAssetException):
        relation = Relationship(relation_type, [], a2)


def test_invalid_target_asset_object_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_1.publish()
    asset_type_2.publish()
    a1 = Asset("Test_Asset_1", asset_type_1, {})
    a2 = Asset("Test_Asset_1", asset_type_2, {})
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(InvalidRelationshipAssetException):
        relation = Relationship(relation_type, a1, [])
