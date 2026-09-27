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
