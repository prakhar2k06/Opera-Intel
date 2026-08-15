from collections import defaultdict

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
        self.assets: set = set()
        self.relationships: set = set()

        self.incoming: dict = defaultdict(list)
        self.outgoing: dict = defaultdict(list)

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

    def get_assets(self) -> set:
        return set(self.assets)

    def get_relationships(self) -> set:
        return set(self.relationships)

    def get_outgoing(self, asset: Asset) -> list:
        self._validate_asset_in_graph(asset)

        return list(self.outgoing[asset])

    def get_incoming(self, asset: Asset) -> list:
        self._validate_asset_in_graph(asset)

        return list(self.incoming[asset])

    def get_neighbors(self, asset: Asset) -> set:
        self._validate_asset_in_graph(asset)

        neighbors = set()

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
    ) -> list:
        self._validate_asset_in_graph(asset)

        return [
            self._get_other_asset(asset, relationship)
            for relationship in self.incoming[asset]
            if relationship.relationship_type == relationship_type
        ]

    def _validate_asset_in_graph(self, asset: Asset) -> None:
        if not isinstance(asset, Asset):
            raise InvalidGraphAssetException

        if asset not in self.assets:
            raise AssetNotInGraphException

    @staticmethod
    def _get_other_asset(asset: Asset, relationship: Relationship) -> Asset:
        if relationship.source_asset is asset:
            return relationship.target_asset

        return relationship.source_asset
