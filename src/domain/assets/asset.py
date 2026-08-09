from .asset_type import AssetType
from .exceptions import (
    InvalidPropertyValueException,
    MissingPropertyException,
    UnknownPropertyException,
    UnpublishedAssetTypeException,
)
from .sentinel import Sentinel


class Asset:
    def __init__(self, name: str, asset_type: AssetType, properties: dict) -> None:
        if not asset_type.is_published:
            raise UnpublishedAssetTypeException

        self.name: str = name
        self.asset_type: AssetType = asset_type
        self.properties: dict = {}

        for property_name in properties:
            if property_name not in self.asset_type.properties:
                raise UnknownPropertyException

        for property_name, property_definition in self.asset_type.properties.items():
            if property_name in properties:
                value = properties[property_name]

                if not property_definition.property_type.validate(value):
                    raise InvalidPropertyValueException

                self.properties[property_name] = value

            elif property_definition.default_value is not Sentinel.UNDEFINED:
                if not property_definition.property_type.validate(
                    property_definition.default_value
                ):
                    raise InvalidPropertyValueException

                self.properties[property_name] = property_definition.default_value

            elif property_definition.required:
                raise MissingPropertyException

            else:
                self.properties[property_name] = None

        self.asset_type.publish()
