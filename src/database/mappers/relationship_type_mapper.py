from ...domain.assets.asset_type import AssetType
from ...domain.relationships.relationship_type import RelationshipType
from ..models.asset_type_model import AssetTypeModel
from ..models.relationship_type_model import RelationshipTypeModel


class RelationshipTypeMapper:
    def to_model(
        self,
        relationship_type: RelationshipType,
        source_asset_type_model: AssetTypeModel,
        target_asset_type_model: AssetTypeModel,
    ) -> RelationshipTypeModel:
        return RelationshipTypeModel(
            id=relationship_type.id,
            name=relationship_type.name,
            source_asset_type=source_asset_type_model,
            target_asset_type=target_asset_type_model,
            is_bidirectional=relationship_type.is_bidirectional,
        )

    def to_domain(
        self,
        relationship_type_model: RelationshipTypeModel,
        source_asset_type: AssetType,
        target_asset_type: AssetType,
    ) -> RelationshipType:
        return RelationshipType(
            id=relationship_type_model.id,
            name=relationship_type_model.name,
            source_type=source_asset_type,
            target_type=target_asset_type,
            is_bidirectional=relationship_type_model.is_bidirectional,
        )
