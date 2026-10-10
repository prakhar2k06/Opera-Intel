from uuid import UUID

from sqlalchemy.orm import Session

from ...database.repositories.asset_type_repository import AssetTypeRepository
from ...database.repositories.relationship_type_repository import (
    RelationshipTypeRepository,
)
from ...domain.assets.asset_type import AssetType
from ...domain.relationships.relationship_type import RelationshipType


class RelationshipTypeService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.relationship_type_repository: RelationshipTypeRepository = (
            RelationshipTypeRepository(session)
        )
        self.asset_type_repository = AssetTypeRepository(session)

    def create(
        self,
        name: str,
        source_type_id: UUID,
        target_type_id: UUID,
        is_bidirectional: bool,
    ) -> RelationshipType:
        with self.session.begin():
            source_type: AssetType = self.asset_type_repository.get_by_id(
                source_type_id
            )
            target_type: AssetType = self.asset_type_repository.get_by_id(
                target_type_id
            )
            relationship_type = RelationshipType(
                name, source_type, target_type, is_bidirectional
            )
            self.relationship_type_repository.save(relationship_type)
        return relationship_type

    def get_by_id(self, relationship_type_id: UUID) -> RelationshipType:
        return self.relationship_type_repository.get_by_id(relationship_type_id)

    def delete(self, relationship_type_id: UUID) -> None:
        with self.session.begin():
            relationship_type: RelationshipType = self.get_by_id(relationship_type_id)
            self.relationship_type_repository.delete(relationship_type)
