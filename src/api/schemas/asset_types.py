from uuid import UUID

from pydantic import BaseModel

from ...domain.assets.property_type import PropertyType


class PropertyResponse(BaseModel):
    property_type: PropertyType
    required: bool
    has_default: bool
    default_value: object | None = None


class StateResponse(BaseModel):
    name: str


class TransitionResponse(BaseModel):
    source_state: StateResponse
    target_state: StateResponse


# class RuleResponse(BaseModel):
#     pass


class AssetTypeResponse(BaseModel):
    id: UUID
    name: str
    is_published: bool
    properties: dict[str, PropertyResponse]
    states: list[StateResponse]
    transitions: list[TransitionResponse]
    initial_state: StateResponse | None
    # rules: list[RuleResponse]


class CreateAssetTypeRequest(BaseModel):
    name: str


class AddPropertyRequest(BaseModel):
    property_name: str
    property_type: PropertyType
    required: bool
    default_value: object | None = None


class AddStateRequest(BaseModel):
    state_name: str


class SetInitialStateRequest(BaseModel):
    state_name: str


class AddTransitionRequest(BaseModel):
    source_state_name: str
    target_state_name: str


# class AddRuleRequest(BaseModel):
#     pass
