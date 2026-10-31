from datetime import datetime

from ...application.definitions.rule_definition import (
    AndConditionDefinition,
    ConditionDefinition,
    OrConditionDefinition,
    PropertyComparisonDefinition,
    RuleDefinition,
)
from ...domain.assets.asset_type import AssetType
from ...domain.assets.property import Property
from ...domain.assets.sentinel import Sentinel
from ...domain.assets.state import State
from ...domain.assets.state_transition import StateTransition
from ...domain.events.asset_property_changed_event import AssetPropertyChangedEvent
from ...domain.events.asset_state_changed_event import AssetStateChangedEvent
from ...domain.events.domain_event import DomainEvent
from ...domain.rules.action import Action
from ...domain.rules.conditions.and_condition import AndCondition
from ...domain.rules.conditions.comparison import Comparison
from ...domain.rules.conditions.condition import Condition
from ...domain.rules.conditions.or_condition import OrCondition
from ...domain.rules.conditions.property_comparison_condition import (
    PropertyComparisonCondition,
)
from ...domain.rules.rule import Rule
from ...domain.rules.trigger import Trigger
from ..schemas.asset_types import (
    ActionResponse,
    AddPropertyRequest,
    AddRuleRequest,
    AddStateRequest,
    AndConditionRequest,
    AndConditionResponse,
    AssetTypeResponse,
    ConditionRequest,
    ConditionResponse,
    OrConditionRequest,
    OrConditionResponse,
    PropertyComparisonConditionRequest,
    PropertyComparisonConditionResponse,
    PropertyResponse,
    RuleResponse,
    StateResponse,
    TransitionResponse,
    TriggerResponse,
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


def trigger_to_response(trigger: Trigger) -> TriggerResponse:
    event_to_name: dict[type[DomainEvent], str] = {
        AssetPropertyChangedEvent: "asset_property_changed",
        AssetStateChangedEvent: "asset_state_changed",
    }

    trigger_event: str | None = event_to_name.get(trigger.trigger_event)

    if not trigger_event:
        raise ValueError(f"Unsupported trigger event -> {trigger.trigger_event}")

    return TriggerResponse(trigger_event=trigger_event)


def action_to_response(action: Action) -> ActionResponse:
    return ActionResponse(transition_to=state_to_response(action.transition_to))


def condition_to_response(condition: Condition) -> ConditionResponse:
    comparison_to_name: dict[Comparison, str] = {
        Comparison.EQUAL: "equal",
        Comparison.NOT_EQUAL: "not_equal",
        Comparison.GREATER_THAN: "greater_than",
        Comparison.GREATER_THAN_OR_EQUAL: "greater_than_or_equal",
        Comparison.LESS_THAN: "less_than",
        Comparison.LESS_THAN_OR_EQUAL: "less_than_or_equal",
        Comparison.CONTAINS: "contains",
        Comparison.STARTS_WITH: "starts_with",
        Comparison.ENDS_WITH: "ends_with",
    }

    if isinstance(condition, PropertyComparisonCondition):
        comparison_name: str | None = comparison_to_name.get(condition.comparison)

        if not comparison_name:
            raise ValueError(f"Unsupported comparison -> {condition.comparison}")

        value: object = condition.value

        if isinstance(value, datetime):
            value = value.isoformat()

        return PropertyComparisonConditionResponse(
            type="property_comparison",
            property=condition.property.name,
            comparison=comparison_name,
            value=value,
        )

    elif isinstance(condition, OrCondition):
        return OrConditionResponse(
            type="or",
            left=condition_to_response(condition.condition_1),
            right=condition_to_response(condition.condition_2),
        )

    elif isinstance(condition, AndCondition):
        return AndConditionResponse(
            type="and",
            left=condition_to_response(condition.condition_1),
            right=condition_to_response(condition.condition_2),
        )

    raise ValueError(f"Unsupported Condition -> {type(condition)}")


def rule_to_response(rule: Rule) -> RuleResponse:
    return RuleResponse(
        id=rule.id,
        trigger=trigger_to_response(rule.trigger),
        condition=condition_to_response(rule.condition),
        action=action_to_response(rule.action),
        priority=rule.priority,
    )


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
        rules=[rule_to_response(rule) for rule in asset_type.rules],
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


def condition_request_to_definition(request: ConditionRequest) -> ConditionDefinition:
    name_to_comparison: dict[str, Comparison] = {
        "equal": Comparison.EQUAL,
        "not_equal": Comparison.NOT_EQUAL,
        "greater_than": Comparison.GREATER_THAN,
        "greater_than_or_equal": Comparison.GREATER_THAN_OR_EQUAL,
        "less_than": Comparison.LESS_THAN,
        "less_than_or_equal": Comparison.LESS_THAN_OR_EQUAL,
        "contains": Comparison.CONTAINS,
        "starts_with": Comparison.STARTS_WITH,
        "ends_with": Comparison.ENDS_WITH,
    }

    if isinstance(request, PropertyComparisonConditionRequest):
        comparison: Comparison = name_to_comparison.get(request.comparison)

        if not comparison:
            raise ValueError(f"Unsupported comparison -> {request.comparison}")

        return PropertyComparisonDefinition(request.property, comparison, request.value)

    elif isinstance(request, AndConditionRequest):
        return AndConditionDefinition(
            left=condition_request_to_definition(request.left),
            right=condition_request_to_definition(request.right),
        )

    elif isinstance(request, OrConditionRequest):
        return OrConditionDefinition(
            left=condition_request_to_definition(request.left),
            right=condition_request_to_definition(request.right),
        )

    raise ValueError("Unsupported condition request")


def add_rule_request_to_definition(request: AddRuleRequest) -> RuleDefinition:
    name_to_event: dict[str, type[DomainEvent]] = {
        "asset_property_changed": AssetPropertyChangedEvent,
        "asset_state_changed": AssetStateChangedEvent,
    }

    trigger_event: type[DomainEvent] | None = name_to_event.get(request.trigger)

    if not trigger_event:
        raise ValueError(f"Unsupported trigger event -> {request.trigger}")

    condition: ConditionDefinition = condition_request_to_definition(request.condition)

    return RuleDefinition(
        trigger_event, condition, request.target_state_name, request.priority
    )
