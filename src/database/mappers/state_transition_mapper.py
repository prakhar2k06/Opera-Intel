from src.database.models.state_model import StateModel
from src.domain.assets.state import State

from ...domain.assets.state_transition import StateTransition
from ..models.state_transition_model import StateTransitionModel


class StateTransitionMapper:
    def to_model(
        self,
        state_transition: StateTransition,
        source_state_model: StateModel,
        target_state_model: StateModel,
    ) -> StateTransitionModel:
        return StateTransitionModel(
            source_state=source_state_model,
            target_state=target_state_model,
        )

    def to_domain(
        self,
        state_transition_model: StateTransitionModel,
        source_state: State,
        target_state: State,
    ) -> StateTransition:
        return StateTransition(source=source_state, target=target_state)
