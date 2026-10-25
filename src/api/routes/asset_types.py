from uuid import UUID

from fastapi import APIRouter

from ...domain.assets.asset_type import AssetType
from ...domain.assets.property import Property
from ...domain.assets.state import State
from ..dependencies import AssetTypeServiceDep
from ..mappers.asset_types import (
    add_property_request_to_domain,
    add_state_request_to_domain,
    asset_type_to_response,
)
from ..schemas.asset_types import (
    AddPropertyRequest,
    # AddRuleRequest,
    AddStateRequest,
    AddTransitionRequest,
    AssetTypeResponse,
    CreateAssetTypeRequest,
    SetInitialStateRequest,
)

router = APIRouter(prefix="/asset-types", tags=["asset-types"])


@router.post("/")
def create_asset_type(
    request: CreateAssetTypeRequest, asset_type_service: AssetTypeServiceDep
) -> AssetTypeResponse:
    asset_type: AssetType = asset_type_service.create(request.name)
    return asset_type_to_response(asset_type)


@router.get("/{asset_type_id}")
def get_asset_type(
    asset_type_id: UUID, asset_type_service: AssetTypeServiceDep
) -> AssetTypeResponse:
    asset_type: AssetType = asset_type_service.get_by_id(asset_type_id)
    return asset_type_to_response(asset_type)


@router.post("/{asset_type_id}/properties")
def add_property(
    asset_type_id: UUID,
    request: AddPropertyRequest,
    asset_type_service: AssetTypeServiceDep,
) -> AssetTypeResponse:
    property: Property = add_property_request_to_domain(request)
    asset_type: AssetType = asset_type_service.add_property(asset_type_id, property)
    return asset_type_to_response(asset_type)


@router.post("/{asset_type_id}/states")
def add_state(
    asset_type_id: UUID,
    request: AddStateRequest,
    asset_type_service: AssetTypeServiceDep,
) -> AssetTypeResponse:
    state: State = add_state_request_to_domain(request)
    asset_type: AssetType = asset_type_service.add_state(asset_type_id, state)
    return asset_type_to_response(asset_type)


@router.patch("/{asset_type_id}/initial-state")
def set_initial_state(
    asset_type_id: UUID,
    request: SetInitialStateRequest,
    asset_type_service: AssetTypeServiceDep,
) -> AssetTypeResponse:
    asset_type: AssetType = asset_type_service.set_initial_state(
        asset_type_id, request.state_name
    )
    return asset_type_to_response(asset_type)


@router.post("/{asset_type_id}/transitions")
def add_transition(
    asset_type_id: UUID,
    request: AddTransitionRequest,
    asset_type_service: AssetTypeServiceDep,
) -> AssetTypeResponse:
    asset_type: AssetType = asset_type_service.add_transition(
        asset_type_id, request.source_state_name, request.target_state_name
    )
    return asset_type_to_response(asset_type)


# @router.post("/{asset_type_id}/rules")
# async def add_rule(asset_type_id: UUID, request: AddRuleRequest, asset_type_service: AssetTypeServiceDep) -> AssetTypeResponse:


@router.post("/{asset_type_id}/publish")
def publish(
    asset_type_id: UUID, asset_type_service: AssetTypeServiceDep
) -> AssetTypeResponse:
    asset_type: AssetType = asset_type_service.publish(asset_type_id)
    return asset_type_to_response(asset_type)


@router.delete("/{asset_type_id}")
def delete(asset_type_id: UUID, asset_type_service: AssetTypeServiceDep) -> None:
    asset_type_service.delete(asset_type_id)
