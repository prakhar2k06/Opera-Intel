from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.assets.asset_type import AssetType

from ...domain.relationships.relationship_type import RelationshipType
from ..mappers.relationship_type_mapper import RelationshipTypeMapper
from ..models.asset_type_model import AssetTypeModel
from ..models.relationship_type_model import RelationshipTypeModel
from .asset_type_repository import AssetTypeRepository
from .exceptions import AssetTypeNotFoundException, RelationshipTypeNotFoundException


class RelationshipTypeRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.relationship_type_mapper = RelationshipTypeMapper()
        self.asset_type_repository = AssetTypeRepository(session)

    def save(self, relationship_type: RelationshipType) -> None:
        relationship_type_model: RelationshipTypeModel | None = self.session.get(
            RelationshipTypeModel,
            relationship_type.id,
        )

        if not relationship_type_model:
            source_asset_type_model: AssetTypeModel | None = self.session.get(
                AssetTypeModel,
                relationship_type.source_type.id,
            )

            if not source_asset_type_model:
                raise AssetTypeNotFoundException

            target_asset_type_model: AssetTypeModel | None = self.session.get(
                AssetTypeModel,
                relationship_type.target_type.id,
            )

            if not target_asset_type_model:
                raise AssetTypeNotFoundException

            relationship_type_model = self.relationship_type_mapper.to_model(
                relationship_type,
                source_asset_type_model,
                target_asset_type_model,
            )

            self.session.add(relationship_type_model)

        else:
            if relationship_type.name != relationship_type_model.name:
                raise ValueError("Existing RelationshipType name does not match")

            if (
                relationship_type.source_type.id
                != relationship_type_model.source_asset_type_id
            ):
                raise ValueError(
                    "Existing RelationshipType source AssetType does not match"
                )

            if (
                relationship_type.target_type.id
                != relationship_type_model.target_asset_type_id
            ):
                raise ValueError(
                    "Existing RelationshipType target AssetType does not match"
                )

            if (
                relationship_type.is_bidirectional
                != relationship_type_model.is_bidirectional
            ):
                raise ValueError(
                    "Existing RelationshipType bidirectionality does not match"
                )

    def get_by_id(self, relationship_type_id: UUID) -> RelationshipType:
        relationship_type_model: RelationshipTypeModel | None = self.session.get(
            RelationshipTypeModel, relationship_type_id
        )

        if not relationship_type_model:
            raise RelationshipTypeNotFoundException

        source_asset_type: AssetType = self.asset_type_repository.get_by_id(
            relationship_type_model.source_asset_type_id
        )
        target_asset_type: AssetType = self.asset_type_repository.get_by_id(
            relationship_type_model.target_asset_type_id
        )

        return self.relationship_type_mapper.to_domain(
            relationship_type_model, source_asset_type, target_asset_type
        )

    def delete(self, relationship_type: RelationshipType) -> None:
        relationship_type_model: RelationshipTypeModel | None = self.session.get(
            RelationshipTypeModel, relationship_type.id
        )

        if not relationship_type_model:
            raise RelationshipTypeNotFoundException

        self.session.delete(relationship_type_model)
