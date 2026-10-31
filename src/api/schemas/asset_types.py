from typing import Annotated, Literal, TypeAlias
from uuid import UUID

from pydantic import BaseModel, Field

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


class TriggerResponse(BaseModel):
    trigger_event: str


class PropertyComparisonConditionResponse(BaseModel):
    type: Literal["property_comparison"] = "property_comparison"
    property: str
    comparison: str
    value: object


class AndConditionResponse(BaseModel):
    type: Literal["and"] = "and"
    left: "ConditionResponse"
    right: "ConditionResponse"


class OrConditionResponse(BaseModel):
    type: Literal["or"] = "or"
    left: "ConditionResponse"
    right: "ConditionResponse"


ConditionResponse: TypeAlias = Annotated[
    PropertyComparisonConditionResponse | AndConditionResponse | OrConditionResponse,
    Field(discriminator="type"),
]

AndConditionResponse.model_rebuild()
OrConditionResponse.model_rebuild()


class ActionResponse(BaseModel):
    transition_to: StateResponse


class RuleResponse(BaseModel):
    id: UUID
    trigger: TriggerResponse
    condition: ConditionResponse
    action: ActionResponse
    priority: int


class AssetTypeResponse(BaseModel):
    id: UUID
    name: str
    is_published: bool
    properties: dict[str, PropertyResponse]
    states: list[StateResponse]
    transitions: list[TransitionResponse]
    initial_state: StateResponse | None
    rules: list[RuleResponse]


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


class PropertyComparisonConditionRequest(BaseModel):
    type: Literal["property_comparison"] = "property_comparison"
    property: str
    comparison: Literal[
        "equal",
        "not_equal",
        "greater_than",
        "greater_than_or_equal",
        "less_than",
        "less_than_or_equal",
        "contains",
        "starts_with",
        "ends_with",
    ]
    value: object


class AndConditionRequest(BaseModel):
    type: Literal["and"] = "and"
    left: "ConditionRequest"
    right: "ConditionRequest"


class OrConditionRequest(BaseModel):
    type: Literal["or"] = "or"
    left: "ConditionRequest"
    right: "ConditionRequest"


ConditionRequest: TypeAlias = Annotated[
    PropertyComparisonConditionRequest | AndConditionRequest | OrConditionRequest,
    Field(discriminator="type"),
]


AndConditionRequest.model_rebuild()
OrConditionRequest.model_rebuild()


class AddRuleRequest(BaseModel):
    trigger: Literal[
        "asset_property_changed",
        "asset_state_changed",
    ]
    condition: ConditionRequest
    target_state_name: str
    priority: int
