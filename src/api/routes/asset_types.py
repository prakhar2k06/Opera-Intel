from fastapi import APIRouter

from ..dependencies import AssetTypeServiceDep

router = APIRouter(prefix="/asset_types", tags=["asset_types"])


@router.post("/")
async def create_asset(name: str, asset_type_service: AssetTypeServiceDep):
    asset_type_service.create(name)
