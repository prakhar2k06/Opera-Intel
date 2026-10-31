from ...domain.relationships.relationship_type import RelationshipType
from ..schemas.relationship_types import RelationshipTypeResponse


def relationship_type_to_response(
    relationship_type: RelationshipType,
) -> RelationshipTypeResponse:
    return RelationshipTypeResponse(
        id=relationship_type.id,
        name=relationship_type.name,
        source_type_id=relationship_type.source_type.id,
        target_type_id=relationship_type.target_type.id,
        is_bidirectional=relationship_type.is_bidirectional,
    )
