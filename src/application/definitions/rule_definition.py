from dataclasses import dataclass
from typing import TypeAlias

from ...domain.events.domain_event import DomainEvent
from ...domain.rules.conditions.comparison import Comparison


@dataclass(frozen=True)
class PropertyComparisonDefinition:
    property_name: str
    comparison: Comparison
    value: object


@dataclass(frozen=True)
class AndConditionDefinition:
    left: "ConditionDefinition"
    right: "ConditionDefinition"


@dataclass(frozen=True)
class OrConditionDefinition:
    left: "ConditionDefinition"
    right: "ConditionDefinition"


ConditionDefinition: TypeAlias = (
    PropertyComparisonDefinition | AndConditionDefinition | OrConditionDefinition
)


@dataclass(frozen=True)
class RuleDefinition:
    trigger: type[DomainEvent]
    condition: ConditionDefinition
    target_state_name: str
    priority: int
