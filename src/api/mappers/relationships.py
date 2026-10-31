from ...domain.relationships.relationship import Relationship
from ..schemas.relationships import RelationshipResponse


def relationship_to_response(relationship: Relationship) -> RelationshipResponse:
    return RelationshipResponse(
        id=relationship.id,
        relationship_type_id=relationship.relationship_type.id,
        source_asset_id=relationship.source_asset.id,
        target_asset_id=relationship.target_asset.id,
    )
