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


def test_is_reachable_returns_true_when_path_exists() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, b, c))

    assert graph.is_reachable(a, c) is True


def test_is_reachable_returns_false_when_path_does_not_exist() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))

    assert graph.is_reachable(a, c) is False


def test_is_reachable_respects_direction() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(relationship_type, a, b))

    assert graph.is_reachable(a, b) is True
    assert graph.is_reachable(b, a) is False


def test_is_reachable_works_with_bidirectional_relationship() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    relationship_type = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(relationship_type, a, b))

    assert graph.is_reachable(a, b) is True
    assert graph.is_reachable(b, a) is True


def test_is_reachable_filters_relationship_types() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(contains, a, b))
    graph.add_relationship(Relationship(depends_on, b, c))

    assert graph.is_reachable(a, c) is True
    assert graph.is_reachable(a, c, {contains}) is False
    assert graph.is_reachable(a, c, {contains, depends_on}) is True


def test_is_reachable_with_empty_relationship_type_set_returns_false() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(relationship_type, a, b))

    assert graph.is_reachable(a, b, set()) is False


def test_is_reachable_to_self_returns_true() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})

    graph = OperationalGraph()
    graph.add_asset(a)

    assert graph.is_reachable(a, a) is True


def test_get_downstream_returns_all_reachable_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, a, c))
    graph.add_relationship(Relationship(relationship_type, b, d))

    assert graph.get_downstream(a) == {b, c, d}


def test_get_downstream_does_not_include_source() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(relationship_type, a, b))

    assert a not in graph.get_downstream(a)


def test_get_downstream_filters_relationship_types() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(contains, a, b))
    graph.add_relationship(Relationship(contains, b, c))
    graph.add_relationship(Relationship(depends_on, b, d))

    assert graph.get_downstream(a, {contains}) == {b, c}
    assert graph.get_downstream(a, {depends_on}) == set()
    assert graph.get_downstream(a, {contains, depends_on}) == {b, c, d}


def test_get_upstream_returns_all_reachable_assets() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, c))
    graph.add_relationship(Relationship(relationship_type, b, c))
    graph.add_relationship(Relationship(relationship_type, c, d))

    assert graph.get_upstream(d) == {a, b, c}


def test_get_upstream_does_not_include_source() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(relationship_type, a, b))

    assert b not in graph.get_upstream(b)


def test_get_upstream_filters_relationship_types() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(contains, a, b))
    graph.add_relationship(Relationship(contains, b, c))
    graph.add_relationship(Relationship(depends_on, d, c))

    assert graph.get_upstream(c, {contains}) == {a, b}
    assert graph.get_upstream(c, {depends_on}) == {d}


def test_get_path_returns_shortest_path() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})
    e = Asset("E", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d, e):
        graph.add_asset(asset)

    # Short path: A -> B -> D
    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, b, d))

    # Longer path: A -> C -> E -> D
    graph.add_relationship(Relationship(relationship_type, a, c))
    graph.add_relationship(Relationship(relationship_type, c, e))
    graph.add_relationship(Relationship(relationship_type, e, d))

    assert graph.get_path(a, d) == [a, b, d]


def test_get_path_returns_none_when_target_unreachable() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))

    assert graph.get_path(a, c) is None


def test_get_path_to_self_returns_source() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})

    graph = OperationalGraph()
    graph.add_asset(a)

    assert graph.get_path(a, a) == [a]


def test_get_path_filters_relationship_types() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(contains, a, b))
    graph.add_relationship(Relationship(depends_on, b, c))

    assert graph.get_path(a, c) == [a, b, c]
    assert graph.get_path(a, c, {contains}) is None
    assert graph.get_path(a, c, {contains, depends_on}) == [a, b, c]


def test_traversal_handles_cycle_without_infinite_loop() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, b, c))
    graph.add_relationship(Relationship(relationship_type, c, a))

    assert graph.get_downstream(a) == {b, c}
    assert graph.get_upstream(a) == {b, c}
    assert graph.is_reachable(a, c) is True


def test_has_cycle_returns_false_for_acyclic_graph() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})
    d = Asset("D", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c, d):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, a, c))
    graph.add_relationship(Relationship(relationship_type, b, d))
    graph.add_relationship(Relationship(relationship_type, c, d))

    assert graph.has_cycle() is False


def test_has_cycle_returns_true_for_directed_cycle() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, b, c))
    graph.add_relationship(Relationship(relationship_type, c, a))

    assert graph.has_cycle() is True


def test_single_bidirectional_relationship_is_not_cycle() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})

    connected_to = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )

    graph = OperationalGraph()
    graph.add_asset(a)
    graph.add_asset(b)
    graph.add_relationship(Relationship(connected_to, a, b))

    assert graph.has_cycle() is False


def test_has_cycle_detects_cycle_involving_bidirectional_relationship() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    connected_to = RelationshipType(
        "ConnectedTo",
        asset_type,
        asset_type,
        is_bidirectional=True,
    )
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(connected_to, a, b))
    graph.add_relationship(Relationship(depends_on, b, c))
    graph.add_relationship(Relationship(depends_on, c, a))

    assert graph.has_cycle() is True


def test_has_cycle_filters_relationship_types() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    contains = RelationshipType("Contains", asset_type, asset_type)
    depends_on = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(contains, a, b))
    graph.add_relationship(Relationship(depends_on, b, c))
    graph.add_relationship(Relationship(depends_on, c, a))

    assert graph.has_cycle() is True
    assert graph.has_cycle({depends_on}) is False
    assert graph.has_cycle({contains, depends_on}) is True


def test_has_cycle_with_empty_relationship_type_set_returns_false() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    a = Asset("A", asset_type, {})
    b = Asset("B", asset_type, {})
    c = Asset("C", asset_type, {})

    relationship_type = RelationshipType("DependsOn", asset_type, asset_type)

    graph = OperationalGraph()

    for asset in (a, b, c):
        graph.add_asset(asset)

    graph.add_relationship(Relationship(relationship_type, a, b))
    graph.add_relationship(Relationship(relationship_type, b, c))
    graph.add_relationship(Relationship(relationship_type, c, a))

    assert graph.has_cycle(set()) is False


# -------------------------
# Domain Events
# -------------------------


def test_adding_relationship_emits_event() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Asset_1", asset_type, {})
    asset_2 = Asset("Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "Contains",
        asset_type,
        asset_type,
    )

    relationship = Relationship(
        relationship_type,
        asset_1,
        asset_2,
    )

    graph = OperationalGraph()
    graph.add_asset(asset_1)
    graph.add_asset(asset_2)

    graph.add_relationship(relationship)

    assert len(graph._domain_events) == 1
    assert graph._domain_events[0].relationship is relationship


def test_failed_relationship_addition_emits_no_event() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Asset_1", asset_type, {})
    asset_2 = Asset("Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "Contains",
        asset_type,
        asset_type,
    )

    relationship = Relationship(
        relationship_type,
        asset_1,
        asset_2,
    )

    graph = OperationalGraph()
    graph.add_asset(asset_1)

    with pytest.raises(AssetNotInGraphException):
        graph.add_relationship(relationship)

    assert graph._domain_events == []


def test_graph_pull_domain_events_returns_and_clears_events() -> None:
    asset_type = AssetType("Test")
    asset_type.publish()

    asset_1 = Asset("Asset_1", asset_type, {})
    asset_2 = Asset("Asset_2", asset_type, {})

    relationship_type = RelationshipType(
        "Contains",
        asset_type,
        asset_type,
    )

    relationship = Relationship(
        relationship_type,
        asset_1,
        asset_2,
    )

    graph = OperationalGraph()
    graph.add_asset(asset_1)
    graph.add_asset(asset_2)
    graph.add_relationship(relationship)

    events: list = graph.pull_domain_events()

    assert len(events) == 1
    assert events[0].relationship is relationship
    assert graph.pull_domain_events() == []
