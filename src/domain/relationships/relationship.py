from dataclasses import dataclass

from ..assets.asset import Asset
from .exceptions import (
    InvalidRelationshipAssetException,
    InvalidRelationshipTypeException,
    RelationshipTypeMismatchException,
)
from .relationship_type import RelationshipType


@dataclass(frozen=True)
class Relationship:
    relationship_type: RelationshipType
    source_asset: Asset
    target_asset: Asset

    def __post_init__(self) -> None:
        if not isinstance(self.relationship_type, RelationshipType):
            raise InvalidRelationshipTypeException

        if not isinstance(self.source_asset, Asset) or not isinstance(
            self.target_asset, Asset
        ):
            raise InvalidRelationshipAssetException

        if (self.source_asset.asset_type != self.relationship_type.source_type) or (
            self.target_asset.asset_type != self.relationship_type.target_type
        ):
            raise RelationshipTypeMismatchException
