from fastapi import APIRouter

from ..dependencies import AssetServiceDep

router = APIRouter(prefix="/assets", tags=["assets"])
