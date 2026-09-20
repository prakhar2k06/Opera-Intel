from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ..assets.asset import Asset
from .exceptions import (
    InvalidRelationshipAssetException,
    InvalidRelationshipTypeException,
    RelationshipTypeMismatchException,
)
from .relationship_type import RelationshipType


@dataclass(frozen=True, eq=True)
class Relationship:
    relationship_type: RelationshipType
    source_asset: Asset
    target_asset: Asset
    id: UUID = field(default_factory=uuid4)

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Relationship):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
