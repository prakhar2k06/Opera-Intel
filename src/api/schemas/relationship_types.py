from uuid import UUID

from pydantic import BaseModel


class RelationshipTypeResponse(BaseModel):
    id: UUID
    name: str
    source_type_id: UUID
    target_type_id: UUID
    is_bidirectional: bool


class CreateRelationshipTypeRequest(BaseModel):
    name: str
    source_type_id: UUID
    target_type_id: UUID
    is_bidirectional: bool
