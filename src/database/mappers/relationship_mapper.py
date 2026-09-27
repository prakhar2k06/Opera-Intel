from ...domain.assets.asset import Asset
from ...domain.relationships.relationship import Relationship
from ...domain.relationships.relationship_type import RelationshipType
from ..models.asset_model import AssetModel
from ..models.relationship_model import RelationshipModel
from ..models.relationship_type_model import RelationshipTypeModel


class RelationshipMapper:
    def to_model(
        self,
        relationship: Relationship,
        relationship_type_model: RelationshipTypeModel,
        source_asset_model: AssetModel,
        target_asset_model: AssetModel,
    ) -> RelationshipModel:
        return RelationshipModel(
            id=relationship.id,
            relationship_type=relationship_type_model,
            source_asset=source_asset_model,
            target_asset=target_asset_model,
        )

    def to_domain(
        self,
        relationship_model: RelationshipModel,
        relationship_type: RelationshipType,
        source_asset: Asset,
        target_asset: Asset,
    ) -> Relationship:
        return Relationship(
            id=relationship_model.id,
            relationship_type=relationship_type,
            source_asset=source_asset,
            target_asset=target_asset,
        )
