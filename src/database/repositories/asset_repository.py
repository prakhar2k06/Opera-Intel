from uuid import UUID

from sqlalchemy.orm import Session

from src.database.models.asset_type_model import AssetTypeModel
from src.database.models.state_model import StateModel
from src.domain.assets.state import State

from ...domain.assets.asset import Asset
from ...domain.assets.asset_type import AssetType
from ..mappers.asset_mapper import AssetMapper
from ..models.asset_model import AssetModel
from .asset_type_repository import AssetTypeRepository
from .exceptions import AssetNotFoundException, AssetTypeNotFoundException


class AssetRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.asset_mapper = AssetMapper()
        self.asset_type_repository = AssetTypeRepository(session)

    def save(self, asset: Asset) -> None:
        asset_type_model: AssetTypeModel | None = self.session.get(
            AssetTypeModel,
            asset.asset_type.id,
        )

        if not asset_type_model:
            raise AssetTypeNotFoundException

        current_state_model: StateModel | None = None

        if asset.current_state is not None:
            for state_model in asset_type_model.states:
                if state_model.name == asset.current_state.name:
                    current_state_model = state_model
                    break

            if not current_state_model:
                raise ValueError("Asset has no matching current state")

        asset_model: AssetModel | None = self.session.get(
            AssetModel,
            asset.id,
        )

        if not asset_model:
            asset_model = self.asset_mapper.to_model(
                asset,
                asset_type_model,
                current_state_model,
            )

            self.session.add(asset_model)

        else:
            if asset_model.asset_type_id != asset.asset_type.id:
                raise ValueError("Existing Asset AssetType does not match")

            self.asset_mapper.update_model(
                asset,
                asset_model,
                current_state_model,
            )

    def get_by_id(self, asset_id: UUID) -> Asset:
        asset_model: AssetModel | None = self.session.get(AssetModel, asset_id)

        if not asset_model:
            raise AssetNotFoundException

        asset_type: AssetType = self.asset_type_repository.get_by_id(
            asset_model.asset_type_id
        )

        current_state = None
        if asset_model.current_state:
            for state in asset_type.states:
                if state.name == asset_model.current_state.name:
                    current_state: State = state
                    break

        asset: Asset = self.asset_mapper.to_domain(
            asset_model, asset_type, current_state
        )
        return asset

    def delete(self, asset: Asset) -> None:
        asset_model: AssetModel | None = self.session.get(AssetModel, asset.id)

        if not asset_model:
            raise AssetNotFoundException

        self.session.delete(asset_model)
