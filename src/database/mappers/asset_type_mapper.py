from uuid import UUID

from src.database.models.rule_model import RuleModel

from ...domain.assets.asset_type import AssetType
from ...domain.assets.property import Property
from ...domain.assets.state import State
from ...domain.assets.state_transition import StateTransition
from ...domain.rules.rule import Rule
from ..models.asset_type_model import AssetTypeModel
from ..models.property_model import PropertyModel
from ..models.state_model import StateModel
from ..models.state_transition_model import StateTransitionModel
from .property_mapper import PropertyMapper
from .rule_mapper import RuleMapper
from .state_mapper import StateMapper
from .state_transition_mapper import StateTransitionMapper


class AssetTypeMapper:
    def __init__(self) -> None:
        self.property_mapper = PropertyMapper()
        self.state_mapper = StateMapper()
        self.state_transition_mapper = StateTransitionMapper()
        self.rule_mapper = RuleMapper()

    def to_model(self, asset_type: AssetType) -> AssetTypeModel:
        model = AssetTypeModel(
            id=asset_type.id,
            name=asset_type.name,
            is_published=asset_type.is_published,
        )

        for property in asset_type.properties.values():
            property_model: PropertyModel = self.property_mapper.to_model(property)
            model.properties.append(property_model)

        state_models: dict = {}

        for state in asset_type.states:
            state_model: StateModel = self.state_mapper.to_model(state)
            state_models[state] = state_model
            model.states.append(state_model)

        if asset_type.initial_state is not None:
            model.initial_state = state_models[asset_type.initial_state]

        for transition in asset_type.transitions:
            source_state_model: StateModel = state_models[transition.source]
            target_state_model: StateModel = state_models[transition.target]
            transition_model: StateTransitionModel = (
                self.state_transition_mapper.to_model(
                    transition,
                    source_state_model,
                    target_state_model,
                )
            )

            model.transitions.append(transition_model)

        for rule in asset_type.rules:
            target_state_model = state_models[rule.action.transition_to]
            rule_model: RuleModel = self.rule_mapper.to_model(
                rule,
                target_state_model,
            )

            model.rules.append(rule_model)

        return model

    def to_domain(self, asset_type_model: AssetTypeModel) -> AssetType:
        asset_type = AssetType(name=asset_type_model.name, id=asset_type_model.id)

        properties: dict = {}

        for property_model in asset_type_model.properties:
            property: Property = self.property_mapper.to_domain(property_model)
            properties[property_model.name] = property
            asset_type.add_property(property)

        states: dict = {}

        for state_model in asset_type_model.states:
            state: State = self.state_mapper.to_domain(state_model)
            states[state_model.id] = state
            asset_type.add_state(state)

        if asset_type_model.initial_state is not None:
            asset_type.set_initial_state(states[asset_type_model.initial_state.id])

        for transition_model in asset_type_model.transitions:
            transition: StateTransition = self.state_transition_mapper.to_domain(
                transition_model,
                states[transition_model.source_state.id],
                states[transition_model.target_state.id],
            )
            asset_type.add_transition(transition)

        for rule_model in asset_type_model.rules:
            rule: Rule = self.rule_mapper.to_domain(
                rule_model, states[rule_model.target_state.id], properties
            )
            asset_type.add_rule(rule)

        if asset_type_model.is_published:
            asset_type.publish()

        return asset_type

    def update_model(
        self,
        asset_type: AssetType,
        asset_type_model: AssetTypeModel,
    ) -> AssetTypeModel:
        if not asset_type_model.is_published:
            asset_type_model.name = asset_type.name
            existing_properties: dict[str, PropertyModel] = {
                property_model.name: property_model
                for property_model in asset_type_model.properties
            }

            for name, property in asset_type.properties.items():
                if name in existing_properties:
                    existing_property: PropertyModel = existing_properties[name]
                    mapped_property: PropertyModel = self.property_mapper.to_model(
                        property
                    )

                    if (
                        existing_property.property_type != mapped_property.property_type
                        or existing_property.required != mapped_property.required
                        or existing_property.has_default != mapped_property.has_default
                        or existing_property.default_value
                        != mapped_property.default_value
                    ):
                        raise ValueError(
                            f"Existing property does not match domain property -> {name}"
                        )

                    continue

                property_model: PropertyModel = self.property_mapper.to_model(property)
                asset_type_model.properties.append(property_model)

            for name in existing_properties:
                if name not in asset_type.properties:
                    raise ValueError(
                        f"Persisted property missing from domain AssetType -> {name}"
                    )

            existing_states: dict[str, StateModel] = {
                state_model.name: state_model for state_model in asset_type_model.states
            }

            for state in asset_type.states:
                if state.name in existing_states:
                    continue

                state_model: StateModel = self.state_mapper.to_model(state)
                asset_type_model.states.append(state_model)
                existing_states[state.name] = state_model

            for state_name in existing_states:
                if not any(state.name == state_name for state in asset_type.states):
                    raise ValueError(
                        f"Persisted state missing from domain AssetType -> {state_name}"
                    )

            if asset_type.initial_state is None:
                asset_type_model.initial_state = None
            else:
                asset_type_model.initial_state = existing_states[
                    asset_type.initial_state.name
                ]

            existing_transitions: dict[tuple[str, str], StateTransitionModel] = {
                (
                    transition_model.source_state.name,
                    transition_model.target_state.name,
                ): transition_model
                for transition_model in asset_type_model.transitions
            }

            domain_transitions: set[tuple[str, str]] = {
                (
                    transition.source.name,
                    transition.target.name,
                )
                for transition in asset_type.transitions
            }

            for transition in asset_type.transitions:
                transition_key: tuple[str, str] = (
                    transition.source.name,
                    transition.target.name,
                )

                if transition_key in existing_transitions:
                    continue

                source_state_model: StateModel = existing_states[transition.source.name]

                target_state_model: StateModel = existing_states[transition.target.name]

                transition_model: StateTransitionModel = (
                    self.state_transition_mapper.to_model(
                        transition,
                        source_state_model,
                        target_state_model,
                    )
                )

                asset_type_model.transitions.append(transition_model)

            for transition_key in existing_transitions:
                if transition_key not in domain_transitions:
                    raise ValueError(
                        f"Persisted transition missing from domain AssetType -> "
                        f"{transition_key}"
                    )

            existing_rules: dict[UUID, RuleModel] = {
                rule_model.id: rule_model for rule_model in asset_type_model.rules
            }

            domain_rule_ids: set[UUID] = {rule.id for rule in asset_type.rules}

            for rule in asset_type.rules:
                target_state_model = existing_states[rule.action.transition_to.name]

                if rule.id in existing_rules:
                    existing_rule: RuleModel = existing_rules[rule.id]

                    mapped_rule: RuleModel = self.rule_mapper.to_model(
                        rule,
                        target_state_model,
                    )

                    if (
                        existing_rule.trigger != mapped_rule.trigger
                        or existing_rule.condition != mapped_rule.condition
                        or existing_rule.target_state.name != target_state_model.name
                    ):
                        raise ValueError(
                            f"Existing rule does not match domain rule -> {rule.id}"
                        )

                    continue

                rule_model: RuleModel = self.rule_mapper.to_model(
                    rule,
                    target_state_model,
                )

                asset_type_model.rules.append(rule_model)

            for rule_id in existing_rules:
                if rule_id not in domain_rule_ids:
                    raise ValueError(
                        f"Persisted rule missing from domain AssetType -> {rule_id}"
                    )

            asset_type_model.is_published = asset_type.is_published

            return asset_type_model

        else:
            if not asset_type.is_published:
                raise ValueError("Published AssetType cannot become unpublished")

            if asset_type_model.name != asset_type.name:
                raise ValueError("Published AssetType name does not match")

            existing_properties = {
                property_model.name: property_model
                for property_model in asset_type_model.properties
            }

            if set(existing_properties.keys()) != set(asset_type.properties.keys()):
                raise ValueError("Published AssetType properties do not match")

            for name, property in asset_type.properties.items():
                existing_property = existing_properties[name]
                mapped_property = self.property_mapper.to_model(property)

                if (
                    existing_property.property_type != mapped_property.property_type
                    or existing_property.required != mapped_property.required
                    or existing_property.has_default != mapped_property.has_default
                    or existing_property.default_value != mapped_property.default_value
                ):
                    raise ValueError(
                        f"Published AssetType property does not match -> {name}"
                    )

            existing_states = {
                state_model.name: state_model for state_model in asset_type_model.states
            }

            domain_state_names: set[str] = {state.name for state in asset_type.states}

            if set(existing_states.keys()) != domain_state_names:
                raise ValueError("Published AssetType states do not match")

            persisted_initial_state: str | None = (
                asset_type_model.initial_state.name
                if asset_type_model.initial_state is not None
                else None
            )

            domain_initial_state: str | None = (
                asset_type.initial_state.name
                if asset_type.initial_state is not None
                else None
            )

            if persisted_initial_state != domain_initial_state:
                raise ValueError("Published AssetType initial state does not match")

            persisted_transitions: set[tuple[str, str]] = {
                (
                    transition_model.source_state.name,
                    transition_model.target_state.name,
                )
                for transition_model in asset_type_model.transitions
            }

            domain_transitions = {
                (
                    transition.source.name,
                    transition.target.name,
                )
                for transition in asset_type.transitions
            }

            if persisted_transitions != domain_transitions:
                raise ValueError("Published AssetType transitions do not match")

            existing_rules = {
                rule_model.id: rule_model for rule_model in asset_type_model.rules
            }

            domain_rule_ids = {rule.id for rule in asset_type.rules}

            if set(existing_rules.keys()) != domain_rule_ids:
                raise ValueError("Published AssetType rules do not match")

            for rule in asset_type.rules:
                existing_rule = existing_rules[rule.id]

                target_state_model = existing_states[rule.action.transition_to.name]

                mapped_rule = self.rule_mapper.to_model(
                    rule,
                    target_state_model,
                )

                if (
                    existing_rule.trigger != mapped_rule.trigger
                    or existing_rule.condition != mapped_rule.condition
                    or existing_rule.target_state.name != target_state_model.name
                ):
                    raise ValueError(
                        f"Published AssetType rule does not match -> {rule.id}"
                    )

            return asset_type_model
