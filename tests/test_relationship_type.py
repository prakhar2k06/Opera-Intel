from dataclasses import FrozenInstanceError

import pytest

from src.domain.assets.asset_type import AssetType
from src.domain.relationships.exceptions import (
    InvalidRelationshipTypeException,
)
from src.domain.relationships.relationship_type import RelationshipType


def test_can_create_valid_relationship_type() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)


def test_invalid_source_type_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    with pytest.raises(InvalidRelationshipTypeException):
        relation_type = RelationshipType("Contains", [], asset_type_2)


def test_invalid_target_type_raises() -> None:
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    with pytest.raises(InvalidRelationshipTypeException):
        relation_type = RelationshipType("Contains", asset_type_1, [])


def test_relationship_type_is_immutable():
    asset_type_1 = AssetType("Test_1")
    asset_type_2 = AssetType("Test_2")
    asset_type_3 = AssetType("Test_3")
    relation_type = RelationshipType("Contains", asset_type_1, asset_type_2)
    with pytest.raises(FrozenInstanceError):
        relation_type.source_type = asset_type_3
