from uuid import UUID

from fastapi import APIRouter

from src.domain.relationships.relationship import Relationship

from ..dependencies import RelationshipServiceDep
from ..mappers.relationships import relationship_to_response
from ..schemas.relationships import CreateRelationshipRequest, RelationshipResponse

router = APIRouter(prefix="/relationships", tags=["relationships"])


@router.post("/")
def create_relationship(
    request: CreateRelationshipRequest, relationship_service: RelationshipServiceDep
) -> RelationshipResponse:
    relationship: Relationship = relationship_service.create(
        request.relationship_type_id, request.source_asset_id, request.target_asset_id
    )
    return relationship_to_response(relationship)


@router.get("/{relationship_id}")
def get_relationship(
    relationship_id: UUID, relationship_service: RelationshipServiceDep
) -> RelationshipResponse:
    relationship: Relationship = relationship_service.get_by_id(relationship_id)
    return relationship_to_response(relationship)


@router.delete("/{relationship_id}")
def delete(relationship_id: UUID, relationship_service: RelationshipServiceDep) -> None:
    relationship_service.delete(relationship_id)
