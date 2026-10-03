from uuid import UUID

from sqlalchemy.orm import Session

from ...domain.assets.asset_type import AssetType
from ..mappers.asset_type_mapper import AssetTypeMapper
from ..models.asset_type_model import AssetTypeModel
from .exceptions import AssetTypeNotFoundException


class AssetTypeRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.asset_type_mapper = AssetTypeMapper()

    def save(self, asset_type: AssetType) -> None:
        asset_type_model: AssetTypeModel | None = self.session.get(
            AssetTypeModel,
            asset_type.id,
        )

        if not asset_type_model:
            asset_type_model = self.asset_type_mapper.to_model(asset_type)
            self.session.add(asset_type_model)

        else:
            self.asset_type_mapper.update_model(asset_type, asset_type_model)

    def get_by_id(self, asset_type_id: UUID) -> AssetType:
        asset_type_model: AssetTypeModel | None = self.session.get(
            AssetTypeModel, asset_type_id
        )

        if not asset_type_model:
            raise AssetTypeNotFoundException

        asset_type: AssetType = self.asset_type_mapper.to_domain(asset_type_model)
        return asset_type

    def delete(self, asset_type: AssetType) -> None:
        asset_type_model: AssetTypeModel | None = self.session.get(
            AssetTypeModel, asset_type.id
        )

        if not asset_type_model:
            raise AssetTypeNotFoundException

        self.session.delete(asset_type_model)
