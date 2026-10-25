from uuid import UUID

from fastapi import APIRouter

from src.domain.assets.asset import Asset

from ..dependencies import AssetServiceDep
from ..mappers.assets import asset_to_response
from ..schemas.assets import (
    AssetResponse,
    CreateAssetRequest,
    TransitionRequest,
    UpdatePropertyRequest,
)

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/")
def create_asset(
    request: CreateAssetRequest, asset_service: AssetServiceDep
) -> AssetResponse:
    asset: Asset = asset_service.create(
        request.name, request.asset_type_id, request.properties
    )
    return asset_to_response(asset)


@router.get("/{asset_id}")
def get_asset(asset_id: UUID, asset_service: AssetServiceDep) -> AssetResponse:
    asset: Asset = asset_service.get_by_id(asset_id)
    return asset_to_response(asset)


@router.post("/{asset_id}/transitions")
def transition(
    asset_id: UUID, request: TransitionRequest, asset_service: AssetServiceDep
) -> AssetResponse:
    asset: Asset = asset_service.transition(asset_id, request.state_name)
    return asset_to_response(asset)


@router.patch("/{asset_id}/properties")
def update_property(
    asset_id: UUID, request: UpdatePropertyRequest, asset_service: AssetServiceDep
) -> AssetResponse:
    asset: Asset = asset_service.update_property(
        asset_id, request.property_name, request.value
    )
    return asset_to_response(asset)


@router.delete("/{asset_id}")
def delete(asset_id: UUID, asset_service: AssetServiceDep) -> None:
    asset_service.delete(asset_id)
