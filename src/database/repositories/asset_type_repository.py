from sqlalchemy import select

from ...domain.assets.asset_type import AssetType
from ..db import Session
from ..models.asset_type_model import AssetTypeModel


class Asset_Type_Repository:
    def get_asset_type_by_id(self, id):
        with Session() as session:
            with session.begin():
                result = session.get(AssetTypeModel, id)

        return result

    def delete_asset_type_by_id(self, id):
        with Session() as session:
            with session.begin():
                result = session.get(AssetTypeModel, id)
                session.delete(result)

    def save_asset_type(self, asset_type: AssetType):
        obj = AssetTypeModel(asset_type.id, asset_type.name, asset_type.is_published)
        with Session() as session:
            with session.begin():
                session.add(obj)
