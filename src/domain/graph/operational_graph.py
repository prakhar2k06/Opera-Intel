from collections import defaultdict, deque

from ..assets.asset import Asset
from ..relationships.relationship import Relationship
from ..relationships.relationship_type import RelationshipType
from .exceptions import (
    AssetNotInGraphException,
    DuplicateAssetException,
    DuplicateRelationshipException,
    InvalidGraphAssetException,
    InvalidGraphRelationshipException,
)


class OperationalGraph:
    def __init__(self) -> None:
        self.assets: set[Asset] = set()
        self.relationships: set[Relationship] = set()

        self.incoming: dict[Asset, list[Relationship]] = defaultdict(list)
        self.outgoing: dict[Asset, list[Relationship]] = defaultdict(list)

    def add_asset(self, asset: Asset) -> None:
        if not isinstance(asset, Asset):
            raise InvalidGraphAssetException

        if asset in self.assets:
            raise DuplicateAssetException

        self.assets.add(asset)

    def add_relationship(self, relationship: Relationship) -> None:
        if not isinstance(relationship, Relationship):
            raise InvalidGraphRelationshipException

        if relationship in self.relationships:
            raise DuplicateRelationshipException

        if (
            relationship.source_asset not in self.assets
            or relationship.target_asset not in self.assets
        ):
            raise AssetNotInGraphException

        self.relationships.add(relationship)

        self.outgoing[relationship.source_asset].append(relationship)
        self.incoming[relationship.target_asset].append(relationship)

        if relationship.relationship_type.is_bidirectional:
            self.outgoing[relationship.target_asset].append(relationship)
            self.incoming[relationship.source_asset].append(relationship)

    def get_assets(self) -> set[Asset]:
        return set(self.assets)

    def get_relationships(self) -> set[Relationship]:
        return set(self.relationships)

    def get_outgoing(self, asset: Asset) -> list[Relationship]:
        self._validate_asset_in_graph(asset)
        return list(self.outgoing[asset])

    def get_incoming(self, asset: Asset) -> list[Relationship]:
        self._validate_asset_in_graph(asset)
        return list(self.incoming[asset])

    def get_neighbors(self, asset: Asset) -> set[Asset]:
        self._validate_asset_in_graph(asset)

        neighbors: set[Asset] = set()

        for relationship in self.outgoing[asset]:
            neighbors.add(self._get_other_asset(asset, relationship))

        for relationship in self.incoming[asset]:
            neighbors.add(self._get_other_asset(asset, relationship))

        return neighbors

    def get_targets(
        self,
        asset: Asset,
        relationship_type: RelationshipType,
    ) -> list[Asset]:
        self._validate_asset_in_graph(asset)

        return [
            self._get_other_asset(asset, relationship)
            for relationship in self.outgoing[asset]
            if relationship.relationship_type == relationship_type
        ]

    def get_sources(
        self,
        asset: Asset,
        relationship_type: RelationshipType,
    ) -> list[Asset]:
        self._validate_asset_in_graph(asset)

        return [
            self._get_other_asset(asset, relationship)
            for relationship in self.incoming[asset]
            if relationship.relationship_type == relationship_type
        ]

    def is_reachable(
        self,
        source: Asset,
        target: Asset,
        relationship_types: set[RelationshipType] | None = None,
    ) -> bool:
        self._validate_asset_in_graph(source)
        self._validate_asset_in_graph(target)

        q: deque[Asset] = deque([source])
        visited: set[Asset] = {source}

        while q:
            node: Asset = q.popleft()

            if node == target:
                return True

            for relationship in self.outgoing[node]:
                if (
                    relationship_types is not None
                    and relationship.relationship_type not in relationship_types
                ):
                    continue

                neighbor: Asset = self._get_other_asset(node, relationship)

                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)

        return False

    def get_downstream(
        self,
        source: Asset,
        relationship_types: set[RelationshipType] | None = None,
    ) -> set[Asset]:
        self._validate_asset_in_graph(source)

        q: deque[Asset] = deque([source])
        visited: set[Asset] = {source}
        downstream: set[Asset] = set()

        while q:
            node: Asset = q.popleft()

            for relationship in self.outgoing[node]:
                if (
                    relationship_types is not None
                    and relationship.relationship_type not in relationship_types
                ):
                    continue

                neighbor: Asset = self._get_other_asset(node, relationship)

                if neighbor not in visited:
                    visited.add(neighbor)
                    downstream.add(neighbor)
                    q.append(neighbor)

        return downstream

    def get_upstream(
        self,
        source: Asset,
        relationship_types: set[RelationshipType] | None = None,
    ) -> set[Asset]:
        self._validate_asset_in_graph(source)

        q: deque[Asset] = deque([source])
        visited: set[Asset] = {source}
        upstream: set[Asset] = set()

        while q:
            node: Asset = q.popleft()

            for relationship in self.incoming[node]:
                if (
                    relationship_types is not None
                    and relationship.relationship_type not in relationship_types
                ):
                    continue

                neighbor: Asset = self._get_other_asset(node, relationship)

                if neighbor not in visited:
                    visited.add(neighbor)
                    upstream.add(neighbor)
                    q.append(neighbor)

        return upstream

    def get_path(
        self,
        source: Asset,
        target: Asset,
        relationship_types: set[RelationshipType] | None = None,
    ) -> list[Asset] | None:
        self._validate_asset_in_graph(source)
        self._validate_asset_in_graph(target)

        q: deque[Asset] = deque([source])
        visited: set[Asset] = {source}
        parent: dict[Asset, Asset | None] = {source: None}

        while q:
            node: Asset = q.popleft()

            if node == target:
                break

            for relationship in self.outgoing[node]:
                if (
                    relationship_types is not None
                    and relationship.relationship_type not in relationship_types
                ):
                    continue

                neighbor: Asset = self._get_other_asset(node, relationship)

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    q.append(neighbor)

        if target not in visited:
            return None

        path: list[Asset] = []
        current_node: Asset | None = target

        while current_node is not None:
            path.append(current_node)
            current_node = parent[current_node]

        return path[::-1]

    def has_cycle(
        self,
        relationship_types: set[RelationshipType] | None = None,
    ) -> bool:
        visited: set[Asset] = set()

        for asset in self.assets:
            if asset not in visited:
                if self._dfs_cycle(
                    asset,
                    visited,
                    set(),
                    relationship_types,
                    None,
                ):
                    return True

        return False

    def _dfs_cycle(
        self,
        asset: Asset,
        visited: set[Asset],
        active_path: set[Asset],
        relationship_types: set[RelationshipType] | None,
        parent_relationship: Relationship | None,
    ) -> bool:
        visited.add(asset)
        active_path.add(asset)

        for relationship in self.outgoing[asset]:
            if (
                relationship_types is not None
                and relationship.relationship_type not in relationship_types
            ):
                continue

            if (
                relationship is parent_relationship
                and relationship.relationship_type.is_bidirectional
            ):
                continue

            neighbor: Asset = self._get_other_asset(asset, relationship)

            if neighbor in active_path:
                return True

            if neighbor not in visited:
                if self._dfs_cycle(
                    neighbor,
                    visited,
                    active_path,
                    relationship_types,
                    relationship,
                ):
                    return True

        active_path.remove(asset)
        return False

    def _validate_asset_in_graph(self, asset: Asset) -> None:
        if not isinstance(asset, Asset):
            raise InvalidGraphAssetException

        if asset not in self.assets:
            raise AssetNotInGraphException

    @staticmethod
    def _get_other_asset(
        asset: Asset,
        relationship: Relationship,
    ) -> Asset:
        if relationship.source_asset is asset:
            return relationship.target_asset

        return relationship.source_asset
