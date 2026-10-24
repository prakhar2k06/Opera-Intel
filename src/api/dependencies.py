from typing import Annotated, TypeAlias

from fastapi import Depends

from ..application.services.asset_service import AssetService
from ..application.services.asset_type_service import AssetTypeService
from ..application.services.relationship_service import RelationshipService
from ..application.services.relationship_type_service import RelationshipTypeService
from ..database.db import Session


def get_session():
    with Session() as session:
        yield session


SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]


def get_asset_type_service(session: SessionDep) -> AssetTypeService:
    return AssetTypeService(session)


def get_asset_service(session: SessionDep) -> AssetService:
    return AssetService(session)


def get_relationship_type_service(session: SessionDep) -> RelationshipTypeService:
    return RelationshipTypeService(session)


def get_relationship_service(session: SessionDep) -> RelationshipService:
    return RelationshipService(session)


AssetTypeServiceDep: TypeAlias = Annotated[
    AssetTypeService, Depends(get_asset_type_service)
]

AssetServiceDep: TypeAlias = Annotated[AssetService, Depends(get_asset_service)]

RelationshipTypeServiceDep: TypeAlias = Annotated[
    RelationshipTypeService, Depends(get_relationship_type_service)
]

RelationshipServiceDep: TypeAlias = Annotated[
    RelationshipService, Depends(get_relationship_service)
]
