from ...domain.assets.asset import Asset
from ..mappers.asset_types import asset_type_to_response, state_to_response
from ..schemas.assets import AssetResponse


def asset_to_response(asset: Asset) -> AssetResponse:
    return AssetResponse(
        id=asset.id,
        name=asset.name,
        asset_type=asset_type_to_response(asset.asset_type),
        properties=asset.properties,
        current_state=state_to_response(asset.current_state)
        if asset.current_state
        else None,
    )
