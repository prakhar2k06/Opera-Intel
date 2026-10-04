from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.assets.asset import Asset
from src.domain.relationships.relationship_type import RelationshipType

from ...domain.relationships.relationship import Relationship
from ..mappers.relationship_mapper import RelationshipMapper
from ..models.asset_model import AssetModel
from ..models.relationship_model import RelationshipModel
from ..models.relationship_type_model import RelationshipTypeModel
from .asset_repository import AssetRepository
from .exceptions import (
    AssetNotFoundException,
    RelationshipNotFoundException,
    RelationshipTypeNotFoundException,
)
from .relationship_type_repository import RelationshipTypeRepository


class RelationshipRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.relationship_mapper: RelationshipMapper = RelationshipMapper()
        self.asset_repository: AssetRepository = AssetRepository(session)
        self.relationship_type_repository: RelationshipTypeRepository = (
            RelationshipTypeRepository(session)
        )

    def save(self, relationship: Relationship) -> None:
        relationship_model: RelationshipModel | None = self.session.get(
            RelationshipModel,
            relationship.id,
        )

        if not relationship_model:
            relationship_type_model: RelationshipTypeModel | None = self.session.get(
                RelationshipTypeModel,
                relationship.relationship_type.id,
            )

            if not relationship_type_model:
                raise RelationshipTypeNotFoundException

            source_asset_model: AssetModel | None = self.session.get(
                AssetModel,
                relationship.source_asset.id,
            )

            if not source_asset_model:
                raise AssetNotFoundException

            target_asset_model: AssetModel | None = self.session.get(
                AssetModel,
                relationship.target_asset.id,
            )

            if not target_asset_model:
                raise AssetNotFoundException

            relationship_model = self.relationship_mapper.to_model(
                relationship,
                relationship_type_model,
                source_asset_model,
                target_asset_model,
            )

            self.session.add(relationship_model)

        else:
            if (
                relationship.relationship_type.id
                != relationship_model.relationship_type_id
            ):
                raise ValueError(
                    "Existing Relationship RelationshipType does not match"
                )

            if relationship.source_asset.id != relationship_model.source_asset_id:
                raise ValueError("Existing Relationship source Asset does not match")

            if relationship.target_asset.id != relationship_model.target_asset_id:
                raise ValueError("Existing Relationship target Asset does not match")

    def get_by_id(self, relationship_id: UUID) -> Relationship:
        relationship_model: RelationshipModel | None = self.session.get(
            RelationshipModel, relationship_id
        )

        if not relationship_model:
            raise RelationshipNotFoundException

        relationship_type: RelationshipType = (
            self.relationship_type_repository.get_by_id(
                relationship_model.relationship_type_id
            )
        )

        source_asset: Asset = self.asset_repository.get_by_id(
            relationship_model.source_asset_id
        )
        target_asset: Asset = self.asset_repository.get_by_id(
            relationship_model.target_asset_id
        )

        return self.relationship_mapper.to_domain(
            relationship_model, relationship_type, source_asset, target_asset
        )

    def delete(self, relationship: Relationship) -> None:
        relationship_model: RelationshipModel | None = self.session.get(
            RelationshipModel, relationship.id
        )

        if not relationship_model:
            raise RelationshipNotFoundException

        self.session.delete(relationship_model)
