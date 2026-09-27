from ...domain.assets.asset import Asset
from ...domain.assets.asset_type import AssetType
from ...domain.assets.state import State
from ..models.asset_model import AssetModel
from ..models.asset_type_model import AssetTypeModel
from ..models.state_model import StateModel


class AssetMapper:
    def to_model(
        self,
        asset: Asset,
        asset_type_model: AssetTypeModel,
        current_state_model: StateModel | None,
    ) -> AssetModel:
        return AssetModel(
            id=asset.id,
            asset_type=asset_type_model,
            name=asset.name,
            current_state=current_state_model,
            properties=dict(asset.properties),
        )

    def to_domain(
        self,
        asset_model: AssetModel,
        asset_type: AssetType,
        current_state: State | None,
    ) -> Asset:
        asset: Asset = Asset.reconstruct_asset(
            id=asset_model.id,
            asset_type=asset_type,
            name=asset_model.name,
            properties=dict(asset_model.properties),
            current_state=current_state,
        )

        return asset
