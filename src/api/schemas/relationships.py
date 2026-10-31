from uuid import UUID

from pydantic import BaseModel


class RelationshipResponse(BaseModel):
    id: UUID
    relationship_type_id: UUID
    source_asset_id: UUID
    target_asset_id: UUID


class CreateRelationshipRequest(BaseModel):
    relationship_type_id: UUID
    source_asset_id: UUID
    target_asset_id: UUID
