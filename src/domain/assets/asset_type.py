from exceptions import AssetTypeSchemaLockedException, DuplicatePropertyException
from property import Property


class AssetType:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.properties: dict = {}
        self.is_published: bool = False

    def add_property(self, property: Property) -> None:
        if self.is_published:
            raise AssetTypeSchemaLockedException

        if property.name in self.properties:
            raise DuplicatePropertyException

        self.properties[property.name] = property

    def publish(self) -> None:
        self.is_published = True
