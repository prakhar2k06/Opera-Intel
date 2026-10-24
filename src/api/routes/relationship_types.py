from fastapi import APIRouter

from ..dependencies import RelationshipTypeServiceDep

router = APIRouter(prefix="/relationship_types", tags=["relationship_types"])
