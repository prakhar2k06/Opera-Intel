class DuplicatePropertyException(Exception):
    pass


class MissingPropertyException(Exception):
    pass


class UnknownPropertyException(Exception):
    pass


class InvalidPropertyValueException(Exception):
    pass


class AssetTypeSchemaLockedException(Exception):
    pass


class UnpublishedAssetTypeException(Exception):
    pass
