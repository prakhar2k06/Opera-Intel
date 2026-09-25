from ...domain.assets.state import State
from ..models.state_model import StateModel


class StateMapper:
    def to_model(self, state: State) -> StateModel:
        return StateModel(name=state.name)

    def to_domain(self, state_model: StateModel) -> State:
        return State(name=state_model.name)
