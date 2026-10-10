from uuid import UUID

from sqlalchemy.orm import Session

from ...database.repositories.asset_repository import AssetRepository
from ...database.repositories.asset_type_repository import AssetTypeRepository
from ...domain.assets.asset import Asset
from ...domain.assets.asset_type import AssetType
from ...domain.assets.state import State


class AssetService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.asset_repository = AssetRepository(session)
        self.asset_type_repository = AssetTypeRepository(session)

    def create(self, name: str, asset_type_id: UUID, properties: dict) -> Asset:
        with self.session.begin():
            asset_type: AssetType = self.asset_type_repository.get_by_id(asset_type_id)
            asset = Asset(name, asset_type, properties)
            self.asset_repository.save(asset)
        return asset

    def get_by_id(self, asset_id: UUID) -> Asset:
        return self.asset_repository.get_by_id(asset_id)

    def transition(self, asset_id: UUID, state_name: str) -> Asset:
        with self.session.begin():
            asset: Asset = self.get_by_id(asset_id)
            state: State = asset.asset_type.get_state_by_name(state_name)
            asset.transition(state)
            self.asset_repository.save(asset)
        return asset

    def update_property(self, asset_id: UUID, property_name: str, value) -> Asset:
        with self.session.begin():
            asset: Asset = self.get_by_id(asset_id)
            asset.update_property(property_name, value)
            self.asset_repository.save(asset)
        return asset

    def delete(self, asset_id: UUID) -> None:
        with self.session.begin():
            asset: Asset = self.get_by_id(asset_id)
            self.asset_repository.delete(asset)
