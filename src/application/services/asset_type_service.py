from uuid import UUID

from sqlalchemy.orm import Session

from ...database.repositories.asset_type_repository import AssetTypeRepository
from ...domain.assets.asset_type import AssetType
from ...domain.assets.property import Property
from ...domain.assets.state import State
from ...domain.assets.state_transition import StateTransition
from ...domain.rules.rule import Rule


class AssetTypeService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.repository: AssetTypeRepository = AssetTypeRepository(session)

    def create(self, name: str) -> AssetType:
        with self.session.begin():
            asset_type = AssetType(name)
            self.repository.save(asset_type)
        return asset_type

    def get_by_id(self, asset_type_id: UUID) -> AssetType:
        return self.repository.get_by_id(asset_type_id)

    def add_property(self, asset_type_id: UUID, property: Property) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            asset_type.add_property(property)
            self.repository.save(asset_type)
        return asset_type

    def add_state(self, asset_type_id: UUID, state: State) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            asset_type.add_state(state)
            self.repository.save(asset_type)
        return asset_type

    def set_initial_state(self, asset_type_id: UUID, state_name: str) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            state: State = asset_type.get_state_by_name(state_name)
            asset_type.set_initial_state(state)
            self.repository.save(asset_type)
        return asset_type

    def add_transition(
        self, asset_type_id: UUID, source_state_name: str, target_state_name: str
    ) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            source_state: State = asset_type.get_state_by_name(source_state_name)
            target_state: State = asset_type.get_state_by_name(target_state_name)
            transition = StateTransition(source_state, target_state)
            asset_type.add_transition(transition)
            self.repository.save(asset_type)
        return asset_type

    def add_rule(self, asset_type_id: UUID, rule: Rule) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            asset_type.add_rule(rule)
            self.repository.save(asset_type)
        return asset_type

    def publish(self, asset_type_id: UUID) -> AssetType:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            asset_type.publish()
            self.repository.save(asset_type)
        return asset_type

    def delete(self, asset_type_id: UUID) -> None:
        with self.session.begin():
            asset_type: AssetType = self.get_by_id(asset_type_id)
            self.repository.delete(asset_type)
