from ...domain.assets.asset_type import AssetType
from ...domain.assets.property import Property
from ...domain.assets.sentinel import Sentinel
from ...domain.assets.state import State
from ...domain.assets.state_transition import StateTransition
from ...domain.rules.rule import Rule
from ..schemas.asset_types import (
    AddPropertyRequest,
    AddStateRequest,
    AssetTypeResponse,
    PropertyResponse,
    # RuleResponse,
    StateResponse,
    TransitionResponse,
)


def property_to_response(property: Property) -> PropertyResponse:
    has_default: bool = property.default_value != Sentinel.UNDEFINED
    return PropertyResponse(
        property_type=property.property_type,
        required=property.required,
        has_default=has_default,
        default_value=property.default_value if has_default else None,
    )


def state_to_response(state: State) -> StateResponse:
    return StateResponse(name=state.name)


def transition_to_response(transition: StateTransition) -> TransitionResponse:
    return TransitionResponse(
        source_state=state_to_response(transition.source),
        target_state=state_to_response(transition.target),
    )


# def rule_to_response(rule: Rule) -> RuleResponse:
#     pass


def asset_type_to_response(asset_type: AssetType) -> AssetTypeResponse:
    return AssetTypeResponse(
        id=asset_type.id,
        name=asset_type.name,
        is_published=asset_type.is_published,
        properties={
            property_name: property_to_response(property)
            for property_name, property in asset_type.properties.items()
        },
        states=[state_to_response(state) for state in asset_type.states],
        transitions=[
            transition_to_response(transition) for transition in asset_type.transitions
        ],
        initial_state=state_to_response(asset_type.initial_state)
        if asset_type.initial_state
        else None,
        # rules=[rule_to_response(rule) for rule in asset_type.rules],
    )


def add_property_request_to_domain(request: AddPropertyRequest) -> Property:
    return Property(
        request.property_name,
        request.property_type,
        request.required,
        request.default_value
        if "default_value" in request.model_fields_set
        else Sentinel.UNDEFINED,
    )


def add_state_request_to_domain(request: AddStateRequest) -> State:
    return State(request.state_name)
