from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType
from src.domain.assets.state import State
from src.domain.events.asset_property_changed_event import (
    AssetPropertyChangedEvent,
)
from src.domain.events.domain_event import DomainEvent
from src.domain.rules.action import Action
from src.domain.rules.conditions.and_condition import AndCondition
from src.domain.rules.conditions.comparison import Comparison
from src.domain.rules.conditions.or_condition import OrCondition
from src.domain.rules.conditions.property_comparison_condition import (
    PropertyComparisonCondition,
)
from src.domain.rules.exceptions import (
    InvalidActionDefinitionException,
    InvalidConditionDefinitionException,
    InvalidRuleDefinitionException,
    InvalidTriggerDefinitionException,
)
from src.domain.rules.rule import Rule
from src.domain.rules.trigger import Trigger

# -------------------------
# Trigger
# -------------------------


def test_can_create_valid_trigger() -> None:
    trigger = Trigger(DomainEvent)

    assert trigger.trigger_event is DomainEvent


def test_trigger_accepts_domain_event_subclass() -> None:
    trigger = Trigger(AssetPropertyChangedEvent)

    assert trigger.trigger_event is AssetPropertyChangedEvent


def test_trigger_rejects_event_instance() -> None:
    with pytest.raises(InvalidTriggerDefinitionException):
        Trigger(DomainEvent())


def test_trigger_rejects_non_event_class() -> None:
    with pytest.raises(InvalidTriggerDefinitionException):
        Trigger(str)


def test_trigger_is_immutable() -> None:
    trigger = Trigger(DomainEvent)

    with pytest.raises(FrozenInstanceError):
        trigger.trigger_event = AssetPropertyChangedEvent


# -------------------------
# Action
# -------------------------


def test_can_create_valid_action() -> None:
    degraded = State("DEGRADED")

    action = Action(degraded)

    assert action.transition_to == degraded


def test_action_rejects_non_state_target() -> None:
    with pytest.raises(InvalidActionDefinitionException):
        Action("DEGRADED")


def test_action_is_immutable() -> None:
    degraded = State("DEGRADED")
    active = State("ACTIVE")

    action = Action(degraded)

    with pytest.raises(FrozenInstanceError):
        action.transition_to = active


# -------------------------
# Comparison
# -------------------------


def test_equal_comparison() -> None:
    assert Comparison.EQUAL.evaluate(10, 10) is True
    assert Comparison.EQUAL.evaluate(10, 20) is False


def test_not_equal_comparison() -> None:
    assert Comparison.NOT_EQUAL.evaluate(10, 20) is True
    assert Comparison.NOT_EQUAL.evaluate(10, 10) is False


def test_greater_than_comparison() -> None:
    assert Comparison.GREATER_THAN.evaluate(20, 10) is True
    assert Comparison.GREATER_THAN.evaluate(10, 20) is False


def test_greater_than_or_equal_comparison() -> None:
    assert Comparison.GREATER_THAN_OR_EQUAL.evaluate(20, 10) is True
    assert Comparison.GREATER_THAN_OR_EQUAL.evaluate(10, 10) is True
    assert Comparison.GREATER_THAN_OR_EQUAL.evaluate(5, 10) is False


def test_less_than_comparison() -> None:
    assert Comparison.LESS_THAN.evaluate(5, 10) is True
    assert Comparison.LESS_THAN.evaluate(20, 10) is False


def test_less_than_or_equal_comparison() -> None:
    assert Comparison.LESS_THAN_OR_EQUAL.evaluate(5, 10) is True
    assert Comparison.LESS_THAN_OR_EQUAL.evaluate(10, 10) is True
    assert Comparison.LESS_THAN_OR_EQUAL.evaluate(20, 10) is False


def test_contains_comparison() -> None:
    assert Comparison.CONTAINS.evaluate("primary-server", "server") is True
    assert Comparison.CONTAINS.evaluate("primary-server", "database") is False


def test_starts_with_comparison() -> None:
    assert Comparison.STARTS_WITH.evaluate("server-01", "server") is True
    assert Comparison.STARTS_WITH.evaluate("server-01", "node") is False


def test_ends_with_comparison() -> None:
    assert Comparison.ENDS_WITH.evaluate("server-01", "01") is True
    assert Comparison.ENDS_WITH.evaluate("server-01", "02") is False


def test_numeric_comparison_support() -> None:
    for property_type in (
        PropertyType.INTEGER,
        PropertyType.FLOAT,
    ):
        assert Comparison.GREATER_THAN.supports_property_type(property_type) is True
        assert Comparison.CONTAINS.supports_property_type(property_type) is False


def test_datetime_comparison_support() -> None:
    assert Comparison.GREATER_THAN.supports_property_type(PropertyType.DATETIME) is True

    assert Comparison.CONTAINS.supports_property_type(PropertyType.DATETIME) is False


def test_string_comparison_support() -> None:
    assert Comparison.EQUAL.supports_property_type(PropertyType.STRING) is True
    assert Comparison.NOT_EQUAL.supports_property_type(PropertyType.STRING) is True
    assert Comparison.CONTAINS.supports_property_type(PropertyType.STRING) is True
    assert Comparison.STARTS_WITH.supports_property_type(PropertyType.STRING) is True
    assert Comparison.ENDS_WITH.supports_property_type(PropertyType.STRING) is True

    assert Comparison.GREATER_THAN.supports_property_type(PropertyType.STRING) is False


def test_boolean_comparison_support() -> None:
    assert Comparison.EQUAL.supports_property_type(PropertyType.BOOLEAN) is True
    assert Comparison.NOT_EQUAL.supports_property_type(PropertyType.BOOLEAN) is True

    assert Comparison.GREATER_THAN.supports_property_type(PropertyType.BOOLEAN) is False


# -------------------------
# PropertyComparisonCondition
# -------------------------


def test_can_create_valid_property_comparison_condition() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    assert condition.property == temperature
    assert condition.comparison == Comparison.GREATER_THAN
    assert condition.value == 90


def test_condition_rejects_invalid_property() -> None:
    with pytest.raises(InvalidConditionDefinitionException):
        PropertyComparisonCondition(
            "Temperature",
            Comparison.GREATER_THAN,
            90,
        )


def test_condition_rejects_invalid_comparison() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    with pytest.raises(InvalidConditionDefinitionException):
        PropertyComparisonCondition(
            temperature,
            "GREATER_THAN",
            90,
        )


def test_condition_rejects_comparison_not_supported_by_property_type() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    with pytest.raises(InvalidConditionDefinitionException):
        PropertyComparisonCondition(
            temperature,
            Comparison.CONTAINS,
            90,
        )


def test_condition_rejects_wrong_comparison_value_type() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    with pytest.raises(InvalidConditionDefinitionException):
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            "hot",
        )


def test_property_comparison_condition_evaluates_true() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 95},
    )

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    assert condition.evaluate(asset) is True


def test_property_comparison_condition_evaluates_false() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 80},
    )

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    assert condition.evaluate(asset) is False


def test_property_comparison_condition_returns_referenced_property() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    assert condition.get_referenced_properties() == {temperature}


# -------------------------
# AndCondition
# -------------------------


def test_and_condition_evaluates_true_when_both_conditions_true() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_property(pressure)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {
            "Temperature": 95,
            "Pressure": 220,
        },
    )

    condition = AndCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        PropertyComparisonCondition(
            pressure,
            Comparison.GREATER_THAN,
            200,
        ),
    )

    assert condition.evaluate(asset) is True


def test_and_condition_evaluates_false_when_one_condition_false() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_property(pressure)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {
            "Temperature": 95,
            "Pressure": 150,
        },
    )

    condition = AndCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        PropertyComparisonCondition(
            pressure,
            Comparison.GREATER_THAN,
            200,
        ),
    )

    assert condition.evaluate(asset) is False


def test_and_condition_collects_referenced_properties() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)

    condition = AndCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        PropertyComparisonCondition(
            pressure,
            Comparison.GREATER_THAN,
            200,
        ),
    )

    assert condition.get_referenced_properties() == {
        temperature,
        pressure,
    }


# -------------------------
# OrCondition
# -------------------------


def test_or_condition_evaluates_true_when_one_condition_true() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_property(pressure)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {
            "Temperature": 95,
            "Pressure": 150,
        },
    )

    condition = OrCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        PropertyComparisonCondition(
            pressure,
            Comparison.GREATER_THAN,
            200,
        ),
    )

    assert condition.evaluate(asset) is True


def test_or_condition_evaluates_false_when_both_conditions_false() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_property(pressure)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {
            "Temperature": 80,
            "Pressure": 150,
        },
    )

    condition = OrCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        PropertyComparisonCondition(
            pressure,
            Comparison.GREATER_THAN,
            200,
        ),
    )

    assert condition.evaluate(asset) is False


# -------------------------
# Nested Conditions
# -------------------------


def test_nested_conditions_evaluate_correctly() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)
    status = Property("Status", PropertyType.STRING, True)

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_property(pressure)
    asset_type.add_property(status)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {
            "Temperature": 95,
            "Pressure": 150,
            "Status": "FAILED",
        },
    )

    condition = AndCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        OrCondition(
            PropertyComparisonCondition(
                pressure,
                Comparison.GREATER_THAN,
                200,
            ),
            PropertyComparisonCondition(
                status,
                Comparison.EQUAL,
                "FAILED",
            ),
        ),
    )

    assert condition.evaluate(asset) is True


def test_nested_condition_collects_all_referenced_properties() -> None:
    temperature = Property("Temperature", PropertyType.FLOAT, True)
    pressure = Property("Pressure", PropertyType.FLOAT, True)
    status = Property("Status", PropertyType.STRING, True)

    condition = AndCondition(
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        OrCondition(
            PropertyComparisonCondition(
                pressure,
                Comparison.GREATER_THAN,
                200,
            ),
            PropertyComparisonCondition(
                status,
                Comparison.EQUAL,
                "FAILED",
            ),
        ),
    )

    assert condition.get_referenced_properties() == {
        temperature,
        pressure,
        status,
    }


# -------------------------
# Rule
# -------------------------


def test_can_create_valid_rule() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    degraded = State("DEGRADED")

    trigger = Trigger(DomainEvent)

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    action = Action(degraded)

    rule = Rule(
        trigger,
        condition,
        action,
    )

    assert rule.trigger == trigger
    assert rule.condition == condition
    assert rule.action == action


def test_rule_rejects_invalid_trigger() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    degraded = State("DEGRADED")

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    action = Action(degraded)

    with pytest.raises(InvalidRuleDefinitionException):
        Rule(
            "trigger",
            condition,
            action,
        )


def test_rule_rejects_invalid_condition() -> None:
    degraded = State("DEGRADED")

    with pytest.raises(InvalidRuleDefinitionException):
        Rule(
            Trigger(DomainEvent),
            "condition",
            Action(degraded),
        )


def test_rule_rejects_invalid_action() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    condition = PropertyComparisonCondition(
        temperature,
        Comparison.GREATER_THAN,
        90,
    )

    with pytest.raises(InvalidRuleDefinitionException):
        Rule(
            Trigger(DomainEvent),
            condition,
            "action",
        )


def test_rule_is_immutable() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    degraded = State("DEGRADED")

    rule = Rule(
        Trigger(DomainEvent),
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        Action(degraded),
    )

    with pytest.raises(FrozenInstanceError):
        rule.action = Action(State("ACTIVE"))
