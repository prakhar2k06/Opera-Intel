import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.graph.exceptions import (
    AssetNotInGraphException,
    DuplicateAssetException,
    DuplicateRelationshipException,
    InvalidGraphAssetException,
    InvalidGraphRelationshipException,
)
from src.domain.graph.operational_graph import OperationalGraph
from src.domain.relationships.relationship import Relationship
from src.domain.relationships.relationship_type import RelationshipType


def test_can_add_asset() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()
    op_graph.add_asset(asset)

    assert asset in op_graph.get_assets()


def test_invalid_asset_raises() -> None:
    op_graph = OperationalGraph()

    with pytest.raises(InvalidGraphAssetException):
        op_graph.add_asset([])


def test_duplicate_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()
    op_graph.add_asset(asset)

    with pytest.raises(DuplicateAssetException):
        op_graph.add_asset(asset)


def test_can_add_directed_relationship() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert relationship in op_graph.get_relationships()


def test_invalid_relationship_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)

    with pytest.raises(InvalidGraphRelationshipException):
        op_graph.add_relationship([])


def test_duplicate_relationship_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    with pytest.raises(DuplicateRelationshipException):
        op_graph.add_relationship(relationship)


def test_relationship_with_unregistered_source_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_2)

    with pytest.raises(AssetNotInGraphException):
        op_graph.add_relationship(relationship)


def test_relationship_with_unregistered_target_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)

    with pytest.raises(AssetNotInGraphException):
        op_graph.add_relationship(relationship)


def test_get_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)

    assert op_graph.get_assets() == {asset_1, asset_2}


def test_get_relationships() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})
    asset_3 = Asset("Test_Asset_3", asset_type, {})
    asset_4 = Asset("Test_Asset_4", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)

    relationship_1 = Relationship(relationship_type, asset_1, asset_2)
    relationship_2 = Relationship(relationship_type, asset_3, asset_4)

    op_graph = OperationalGraph()

    for asset in (asset_1, asset_2, asset_3, asset_4):
        op_graph.add_asset(asset)

    op_graph.add_relationship(relationship_1)
    op_graph.add_relationship(relationship_2)

    assert op_graph.get_relationships() == {relationship_1, relationship_2}


def test_get_assets_returns_copy() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()
    op_graph.add_asset(asset)

    assets = op_graph.get_assets()
    assets.clear()

    assert asset in op_graph.get_assets()


def test_get_relationships_returns_copy() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    relationships = op_graph.get_relationships()
    relationships.clear()

    assert relationship in op_graph.get_relationships()


def test_get_outgoing_for_directed_relationship() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_outgoing(asset_1) == [relationship]
    assert op_graph.get_outgoing(asset_2) == []


def test_get_incoming_for_directed_relationship() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)
    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_incoming(asset_2) == [relationship]
    assert op_graph.get_incoming(asset_1) == []


def test_get_outgoing_for_unknown_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()

    with pytest.raises(AssetNotInGraphException):
        op_graph.get_outgoing(asset)


def test_get_incoming_for_unknown_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()

    with pytest.raises(AssetNotInGraphException):
        op_graph.get_incoming(asset)


def test_get_neighbors_returns_outgoing_and_incoming_neighbors() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})
    asset_3 = Asset("Test_Asset_3", asset_type, {})

    relationship_type = RelationshipType("Contains", asset_type, asset_type)

    relationship_1 = Relationship(relationship_type, asset_1, asset_2)
    relationship_2 = Relationship(relationship_type, asset_3, asset_1)

    op_graph = OperationalGraph()

    for asset in (asset_1, asset_2, asset_3):
        op_graph.add_asset(asset)

    op_graph.add_relationship(relationship_1)
    op_graph.add_relationship(relationship_2)

    assert op_graph.get_neighbors(asset_1) == {asset_2, asset_3}


def test_get_neighbors_returns_unique_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type_1 = RelationshipType("Contains", asset_type, asset_type)
    relationship_type_2 = RelationshipType("Uses", asset_type, asset_type)

    relationship_1 = Relationship(relationship_type_1, asset_1, asset_2)
    relationship_2 = Relationship(relationship_type_2, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)

    op_graph.add_relationship(relationship_1)
    op_graph.add_relationship(relationship_2)

    assert op_graph.get_neighbors(asset_1) == {asset_2}


def test_get_neighbors_for_unknown_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})

    op_graph = OperationalGraph()

    with pytest.raises(AssetNotInGraphException):
        op_graph.get_neighbors(asset)


def test_get_targets_filters_by_relationship_type() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})
    asset_3 = Asset("Test_Asset_3", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    uses = RelationshipType("Uses", asset_type, asset_type)

    relationship_1 = Relationship(contains, asset_1, asset_2)
    relationship_2 = Relationship(uses, asset_1, asset_3)

    op_graph = OperationalGraph()

    for asset in (asset_1, asset_2, asset_3):
        op_graph.add_asset(asset)

    op_graph.add_relationship(relationship_1)
    op_graph.add_relationship(relationship_2)

    assert op_graph.get_targets(asset_1, contains) == [asset_2]


def test_get_sources_filters_by_relationship_type() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})
    asset_3 = Asset("Test_Asset_3", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    uses = RelationshipType("Uses", asset_type, asset_type)

    relationship_1 = Relationship(contains, asset_1, asset_3)
    relationship_2 = Relationship(uses, asset_2, asset_3)

    op_graph = OperationalGraph()

    for asset in (asset_1, asset_2, asset_3):
        op_graph.add_asset(asset)

    op_graph.add_relationship(relationship_1)
    op_graph.add_relationship(relationship_2)

    assert op_graph.get_sources(asset_3, contains) == [asset_1]


def test_get_targets_for_unknown_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})
    relationship_type = RelationshipType("Contains", asset_type, asset_type)

    op_graph = OperationalGraph()

    with pytest.raises(AssetNotInGraphException):
        op_graph.get_targets(asset, relationship_type)


def test_get_sources_for_unknown_asset_raises() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset = Asset("Test_Asset", asset_type, {})
    relationship_type = RelationshipType("Contains", asset_type, asset_type)

    op_graph = OperationalGraph()

    with pytest.raises(AssetNotInGraphException):
        op_graph.get_sources(asset, relationship_type)


def test_bidirectional_relationship_is_stored_once() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_relationships() == {relationship}


def test_bidirectional_relationship_is_outgoing_from_both_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert relationship in op_graph.get_outgoing(asset_1)
    assert relationship in op_graph.get_outgoing(asset_2)


def test_bidirectional_relationship_is_incoming_to_both_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert relationship in op_graph.get_incoming(asset_1)
    assert relationship in op_graph.get_incoming(asset_2)


def test_bidirectional_get_targets_works_from_both_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_targets(asset_1, relationship_type) == [asset_2]
    assert op_graph.get_targets(asset_2, relationship_type) == [asset_1]


def test_bidirectional_get_sources_works_from_both_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_sources(asset_1, relationship_type) == [asset_2]
    assert op_graph.get_sources(asset_2, relationship_type) == [asset_1]


def test_bidirectional_get_neighbors_works_from_both_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert op_graph.get_neighbors(asset_1) == {asset_2}
    assert op_graph.get_neighbors(asset_2) == {asset_1}


def test_directed_relationship_is_not_indexed_in_reverse() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Test_Asset_1", asset_type, {})
    asset_2 = Asset("Test_Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "Contains",
        asset_type,
        asset_type,
        is_bidirectional=False,
    )

    relationship = Relationship(relationship_type, asset_1, asset_2)

    op_graph = OperationalGraph()
    op_graph.add_asset(asset_1)
    op_graph.add_asset(asset_2)
    op_graph.add_relationship(relationship)

    assert relationship in op_graph.get_outgoing(asset_1)
    assert relationship in op_graph.get_incoming(asset_2)

    assert relationship not in op_graph.get_outgoing(asset_2)
    assert relationship not in op_graph.get_incoming(asset_1)
