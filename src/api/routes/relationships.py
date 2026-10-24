from fastapi import APIRouter

from ..dependencies import RelationshipServiceDep

router = APIRouter(prefix="/relationships", tags=["relationships"])
