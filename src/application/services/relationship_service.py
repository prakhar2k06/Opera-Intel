from uuid import UUID

from sqlalchemy.orm import Session

from ...database.repositories.asset_repository import AssetRepository
from ...database.repositories.relationship_repository import RelationshipRepository
from ...database.repositories.relationship_type_repository import (
    RelationshipTypeRepository,
)
from ...domain.assets.asset import Asset
from ...domain.relationships.relationship import Relationship
from ...domain.relationships.relationship_type import RelationshipType


class RelationshipService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.relationship_repository = RelationshipRepository(session)
        self.relationship_type_repository = RelationshipTypeRepository(session)
        self.asset_repository = AssetRepository(session)

    def create(
        self,
        relationship_type_id: UUID,
        source_asset_id: UUID,
        target_asset_id: UUID,
    ) -> Relationship:
        with self.session.begin():
            relationship_type: RelationshipType = (
                self.relationship_type_repository.get_by_id(relationship_type_id)
            )
            source_asset: Asset = self.asset_repository.get_by_id(source_asset_id)
            target_asset: Asset = self.asset_repository.get_by_id(target_asset_id)
            relationship = Relationship(relationship_type, source_asset, target_asset)
            self.relationship_repository.save(relationship)
        return relationship

    def get_by_id(self, id: UUID) -> Relationship:
        return self.relationship_repository.get_by_id(id)

    def delete(self, relationship_id: UUID) -> None:
        with self.session.begin():
            relationship: Relationship = self.get_by_id(relationship_id)
            self.relationship_repository.delete(relationship)
