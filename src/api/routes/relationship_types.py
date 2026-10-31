from uuid import UUID

from fastapi import APIRouter

from src.domain.relationships.relationship_type import RelationshipType

from ..dependencies import RelationshipTypeServiceDep
from ..mappers.relationship_types import relationship_type_to_response
from ..schemas.relationship_types import (
    CreateRelationshipTypeRequest,
    RelationshipTypeResponse,
)

router = APIRouter(prefix="/relationship_types", tags=["relationship_types"])


@router.post("/")
def create_relationship_type(
    request: CreateRelationshipTypeRequest,
    relationship_type_service: RelationshipTypeServiceDep,
) -> RelationshipTypeResponse:
    relationship_type: RelationshipType = relationship_type_service.create(
        request.name,
        request.source_type_id,
        request.target_type_id,
        request.is_bidirectional,
    )
    return relationship_type_to_response(relationship_type)


@router.get("/{relationship_type_id}")
def get_relationship_type(
    relationship_type_id: UUID, relationship_type_service: RelationshipTypeServiceDep
) -> RelationshipTypeResponse:
    relationship_type: RelationshipType = relationship_type_service.get_by_id(
        relationship_type_id
    )
    return relationship_type_to_response(relationship_type)


@router.delete("/{relationship_type_id}")
def delete(
    relationship_type_id: UUID, relationship_type_service: RelationshipTypeServiceDep
) -> None:
    relationship_type_service.delete(relationship_type_id)
