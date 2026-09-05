from ..rules.rule import Rule
from .exceptions import (
    AssetTypeSchemaLockedException,
    DuplicatePropertyException,
    DuplicateRuleException,
    DuplicateStateException,
    DuplicateTransitionException,
    InitialStateNotSetException,
    InvalidRuleDefinitionException,
    InvalidStateDefinitionException,
    InvalidStateTransitionException,
    PropertyNotInAssetTypeException,
    StateNotInAssetTypeException,
)
from .property import Property
from .state import State
from .state_transition import StateTransition


class AssetType:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.properties: dict[str, Property] = {}
        self.states: set[State] = set()
        self.transitions: set[StateTransition] = set()
        self.rules: set[Rule] = set()
        self.initial_state: State | None = None
        self.is_published: bool = False

    def add_property(self, property: Property) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if property.name in self.properties:
            raise DuplicatePropertyException

        self.properties[property.name] = property

    def add_state(self, state: State) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if not isinstance(state, State):
            raise InvalidStateDefinitionException

        if state in self.states:
            raise DuplicateStateException

        self.states.add(state)

    def set_initial_state(self, state: State) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if not isinstance(state, State):
            raise InvalidStateDefinitionException

        if state not in self.states:
            raise StateNotInAssetTypeException

        self.initial_state = state

    def add_transition(self, transition: StateTransition) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if not isinstance(transition, StateTransition):
            raise InvalidStateTransitionException

        if transition.source not in self.states or transition.target not in self.states:
            raise StateNotInAssetTypeException

        if transition in self.transitions:
            raise DuplicateTransitionException

        self.transitions.add(transition)

    def can_transition(
        self,
        source: State,
        target: State,
    ) -> bool:
        if not isinstance(source, State) or not isinstance(target, State):
            raise InvalidStateDefinitionException

        if source not in self.states or target not in self.states:
            raise StateNotInAssetTypeException

        return StateTransition(source, target) in self.transitions

    def add_rule(self, rule: Rule) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if not isinstance(rule, Rule):
            raise InvalidRuleDefinitionException

        for property in rule.condition.get_referenced_properties():
            if property.name not in self.properties:
                raise PropertyNotInAssetTypeException

            if self.properties[property.name] != property:
                raise PropertyNotInAssetTypeException

        if rule.action.transition_to not in self.states:
            raise StateNotInAssetTypeException

        if rule in self.rules:
            raise DuplicateRuleException

        self.rules.add(rule)

    def publish(self) -> None:
        if self.states and self.initial_state is None:
            raise InitialStateNotSetException

        self.is_published = True
