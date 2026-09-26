from datetime import datetime

from ...database.models.rule_model import RuleModel
from ...domain.assets.property import Property
from ...domain.assets.property_type import PropertyType
from ...domain.assets.state import State
from ...domain.events.asset_property_changed_event import AssetPropertyChangedEvent
from ...domain.events.asset_state_changed_event import AssetStateChangedEvent
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
from ..models.state_model import StateModel


class RuleMapper:
    def __init__(self) -> None:
        self.event_to_name = {
            AssetPropertyChangedEvent: "asset_property_changed",
            AssetStateChangedEvent: "asset_state_changed",
        }

        self.name_to_event = {
            "asset_property_changed": AssetPropertyChangedEvent,
            "asset_state_changed": AssetStateChangedEvent,
        }

        self.comparison_to_name: dict[Comparison, str] = {
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

        self.name_to_comparison: dict[str, Comparison] = {
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

    def rule_condition_to_json(self, condition: Condition) -> dict:
        if isinstance(condition, PropertyComparisonCondition):
            comparison_name: str | None = self.comparison_to_name.get(
                condition.comparison
            )

            if not comparison_name:
                raise ValueError(f"Unsupported comparison -> {condition.comparison}")

            value: object = condition.value

            if isinstance(value, datetime):
                value = value.isoformat()

            return {
                "type": "property_comparison",
                "property": condition.property.name,
                "comparison": comparison_name,
                "value": value,
            }

        elif isinstance(condition, OrCondition):
            return {
                "type": "or",
                "left": self.rule_condition_to_json(condition.condition_1),
                "right": self.rule_condition_to_json(condition.condition_2),
            }

        elif isinstance(condition, AndCondition):
            return {
                "type": "and",
                "left": self.rule_condition_to_json(condition.condition_1),
                "right": self.rule_condition_to_json(condition.condition_2),
            }

        raise ValueError(f"Unsupported Condition -> {type(condition)}")

    def json_to_rule_condition(
        self, json: dict, properties: dict[str, Property]
    ) -> Condition:
        condition_type = json["type"]

        if condition_type == "property_comparison":
            property_name = json["property"]

            if property_name not in properties:
                raise ValueError(f"Rule does not support property -> {property_name}")

            property: Property = properties[property_name]

            comparison_name = json["comparison"]
            comparison: Comparison | None = self.name_to_comparison.get(comparison_name)

            if comparison is None:
                raise ValueError(f"Unsupported comparison -> {comparison_name}")

            value = json["value"]

            if property.property_type == PropertyType.DATETIME and isinstance(
                value, str
            ):
                value: datetime = datetime.fromisoformat(value)

            return PropertyComparisonCondition(
                property=property, comparison=comparison, value=value
            )

        elif condition_type == "or":
            return OrCondition(
                condition_1=self.json_to_rule_condition(json["left"], properties),
                condition_2=self.json_to_rule_condition(json["right"], properties),
            )

        elif condition_type == "and":
            return AndCondition(
                condition_1=self.json_to_rule_condition(json["left"], properties),
                condition_2=self.json_to_rule_condition(json["right"], properties),
            )

        raise ValueError(f"Unsupported condition type -> {condition_type}")

    def to_model(self, rule: Rule, target_state_model: StateModel) -> RuleModel:
        trigger_name: str | None = self.event_to_name.get(rule.trigger.trigger_event)

        if trigger_name is None:
            raise ValueError(
                f"Unsupported trigger event -> {rule.trigger.trigger_event}"
            )

        return RuleModel(
            id=rule.id,
            trigger=trigger_name,
            condition=self.rule_condition_to_json(rule.condition),
            target_state=target_state_model,
        )

    def to_domain(self, rule_model: RuleModel, target_state: State, properties) -> Rule:
        trigger_event = self.name_to_event.get(rule_model.trigger)

        if trigger_event is None:
            raise ValueError(f"Unsupported trigger: {rule_model.trigger}")

        trigger = Trigger(trigger_event=trigger_event)

        condition: Condition = self.json_to_rule_condition(
            rule_model.condition,
            properties,
        )

        action = Action(transition_to=target_state)

        return Rule(
            id=rule_model.id,
            trigger=trigger,
            condition=condition,
            action=action,
        )
