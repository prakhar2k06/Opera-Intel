from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.assets.asset import Asset
from src.domain.relationships.relationship import Relationship
from src.domain.relationships.relationship_type import RelationshipType

from ...database.repositories.asset_repository import AssetRepository
from ...database.repositories.relationship_repository import RelationshipRepository
from ...database.repositories.relationship_type_repository import (
    RelationshipTypeRepository,
)
from ...domain.graph.operational_graph import OperationalGraph


class OperationalGraphService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.asset_repository: AssetRepository = AssetRepository(session)
        self.relationship_repository: RelationshipRepository = RelationshipRepository(
            session
        )
        self.relationship_type_repository: RelationshipTypeRepository = (
            RelationshipTypeRepository(session)
        )

    def get_neighbors(self, asset_id: UUID) -> set[Asset]:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            asset: Asset = self.asset_repository.get_by_id(asset_id)
            return graph.get_neighbors(asset)

    def get_downstream(
        self,
        asset_id: UUID,
        relationship_type_ids: set[UUID] | None = None,
        max_depth: int | None = None,
    ) -> set[tuple[Asset, int]]:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            asset: Asset = self.asset_repository.get_by_id(asset_id)

            relationship_types = None
            if relationship_type_ids:
                relationship_types: set[RelationshipType] = (
                    self._resolve_relationship_types(relationship_type_ids)
                )

            return graph.get_downstream(asset, relationship_types, max_depth)

    def get_upstream(
        self,
        asset_id: UUID,
        relationship_type_ids: set[UUID] | None = None,
        max_depth: int | None = None,
    ) -> set[tuple[Asset, int]]:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            asset: Asset = self.asset_repository.get_by_id(asset_id)

            relationship_types = None
            if relationship_type_ids:
                relationship_types: set[RelationshipType] = (
                    self._resolve_relationship_types(relationship_type_ids)
                )

            return graph.get_upstream(asset, relationship_types, max_depth)

    def get_path(
        self,
        source_id: UUID,
        target_id: UUID,
        relationship_type_ids: set[UUID] | None = None,
    ) -> list[Asset] | None:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            source_asset: Asset = self.asset_repository.get_by_id(source_id)
            target_asset: Asset = self.asset_repository.get_by_id(target_id)

            relationship_types = None
            if relationship_type_ids:
                relationship_types: set[RelationshipType] = (
                    self._resolve_relationship_types(relationship_type_ids)
                )

            return graph.get_path(source_asset, target_asset, relationship_types)

    def is_reachable(
        self,
        source_id: UUID,
        target_id: UUID,
        relationship_type_ids: set[UUID] | None = None,
    ) -> bool:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            source_asset: Asset = self.asset_repository.get_by_id(source_id)
            target_asset: Asset = self.asset_repository.get_by_id(target_id)

            relationship_types = None
            if relationship_type_ids:
                relationship_types: set[RelationshipType] = (
                    self._resolve_relationship_types(relationship_type_ids)
                )

            return graph.is_reachable(source_asset, target_asset, relationship_types)

    def has_cycle(self, relationship_type_ids: set[UUID] | None = None) -> bool:
        with self.session.begin():
            graph: OperationalGraph = self._load_graph()

            relationship_types = None
            if relationship_type_ids:
                relationship_types: set[RelationshipType] = (
                    self._resolve_relationship_types(relationship_type_ids)
                )

            return graph.has_cycle(relationship_types)

    def _load_graph(self) -> OperationalGraph:
        assets: list[Asset] = self.asset_repository.get_all()
        relationships: list[Relationship] = self.relationship_repository.get_all()

        graph: OperationalGraph = OperationalGraph.reconstruct_graph(
            assets, relationships
        )

        return graph

    def _resolve_relationship_types(
        self, relationship_type_ids
    ) -> set[RelationshipType]:
        relationship_types: set[RelationshipType] = {
            self.relationship_type_repository.get_by_id(relationship_type_id)
            for relationship_type_id in relationship_type_ids
        }
        return relationship_types
