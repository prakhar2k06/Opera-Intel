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


class InvalidAssetStateTransitionException(Exception):
    pass


class InvalidTargetStateException(Exception):
    pass


class InvalidRuleDefinitionException(Exception):
    pass


class PropertyNotInAssetTypeException(Exception):
    pass


class DuplicateRuleException(Exception):
    pass
