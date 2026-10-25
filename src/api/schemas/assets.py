from uuid import UUID

from pydantic import BaseModel

from ..schemas.asset_types import AssetTypeResponse, StateResponse


class AssetResponse(BaseModel):
    id: UUID
    name: str
    asset_type: AssetTypeResponse
    properties: dict[str, object]
    current_state: StateResponse | None


class CreateAssetRequest(BaseModel):
    name: str
    asset_type_id: UUID
    properties: dict[str, object]


class TransitionRequest(BaseModel):
    state_name: str


class UpdatePropertyRequest(BaseModel):
    property_name: str
    value: object
