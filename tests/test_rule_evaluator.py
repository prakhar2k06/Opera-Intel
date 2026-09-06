import pytest
from src.domain.rules.rule_evaluator import RuleEvaluator

from src.domain.assets.asset import Asset
from src.domain.assets.asset_type import AssetType
from src.domain.assets.exceptions import InvalidAssetStateTransitionException
from src.domain.assets.property import Property
from src.domain.assets.property_type import PropertyType
from src.domain.assets.state import State
from src.domain.assets.state_transition import StateTransition
from src.domain.events.asset_property_changed_event import AssetPropertyChangedEvent
from src.domain.events.asset_state_changed_event import AssetStateChangedEvent
from src.domain.rules.action import Action
from src.domain.rules.conditions.comparison import Comparison
from src.domain.rules.conditions.property_comparison_condition import (
    PropertyComparisonCondition,
)
from src.domain.rules.rule import Rule
from src.domain.rules.trigger import Trigger


def test_matching_rule_with_true_condition_executes_action() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    active = State("ACTIVE")
    degraded = State("DEGRADED")

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_state(active)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(active)
    asset_type.add_transition(StateTransition(active, degraded))

    rule = Rule(
        Trigger(AssetPropertyChangedEvent),
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        Action(degraded),
    )

    asset_type.add_rule(rule)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 95},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=temperature,
        previous_value=80,
        new_value=95,
    )

    evaluator = RuleEvaluator()
    evaluator.evaluate(event)

    assert asset.current_state == degraded


def test_non_matching_trigger_does_not_execute_action() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    active = State("ACTIVE")
    degraded = State("DEGRADED")

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_state(active)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(active)
    asset_type.add_transition(StateTransition(active, degraded))

    rule = Rule(
        Trigger(AssetStateChangedEvent),
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        Action(degraded),
    )

    asset_type.add_rule(rule)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 95},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=temperature,
        previous_value=80,
        new_value=95,
    )

    evaluator = RuleEvaluator()
    evaluator.evaluate(event)

    assert asset.current_state == active


def test_matching_trigger_with_false_condition_does_not_execute_action() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    active = State("ACTIVE")
    degraded = State("DEGRADED")

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_state(active)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(active)
    asset_type.add_transition(StateTransition(active, degraded))

    rule = Rule(
        Trigger(AssetPropertyChangedEvent),
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        Action(degraded),
    )

    asset_type.add_rule(rule)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 80},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=temperature,
        previous_value=70,
        new_value=80,
    )

    evaluator = RuleEvaluator()
    evaluator.evaluate(event)

    assert asset.current_state == active


def test_invalid_rule_action_propagates_domain_exception() -> None:
    temperature = Property(
        "Temperature",
        PropertyType.FLOAT,
        True,
    )

    active = State("ACTIVE")
    degraded = State("DEGRADED")

    asset_type = AssetType("Test")
    asset_type.add_property(temperature)
    asset_type.add_state(active)
    asset_type.add_state(degraded)
    asset_type.set_initial_state(active)

    rule = Rule(
        Trigger(AssetPropertyChangedEvent),
        PropertyComparisonCondition(
            temperature,
            Comparison.GREATER_THAN,
            90,
        ),
        Action(degraded),
    )

    asset_type.add_rule(rule)
    asset_type.publish()

    asset = Asset(
        "Asset_1",
        asset_type,
        {"Temperature": 95},
    )

    event = AssetPropertyChangedEvent(
        asset=asset,
        property=temperature,
        previous_value=80,
        new_value=95,
    )

    evaluator = RuleEvaluator()

    with pytest.raises(InvalidAssetStateTransitionException):
        evaluator.evaluate(event)
