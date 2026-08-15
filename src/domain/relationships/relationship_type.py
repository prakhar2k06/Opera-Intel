from dataclasses import dataclass

from ..assets.asset_type import AssetType
from .exceptions import InvalidRelationshipTypeException


@dataclass(frozen=True)
class RelationshipType:
    name: str
    source_type: AssetType
    target_type: AssetType
    is_bidirectional: bool = False

    def __post_init__(self) -> None:
        if not (isinstance(self.source_type, AssetType)) or not (
            isinstance(self.target_type, AssetType)
        ):
            raise InvalidRelationshipTypeException

        if not isinstance(self.is_bidirectional, bool):
            raise InvalidRelationshipTypeException
