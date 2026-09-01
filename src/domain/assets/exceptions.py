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


class InvalidStateTransitionException(Exception):
    pass


class InvalidStateDefinitionException(Exception):
    pass


class DuplicateStateException(Exception):
    pass


class DuplicateTransitionException(Exception):
    pass


class StateNotInAssetTypeException(Exception):
    pass


class InitialStateNotSetException(Exception):
    pass
