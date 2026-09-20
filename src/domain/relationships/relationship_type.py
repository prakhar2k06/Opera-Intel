from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ..assets.asset_type import AssetType
from .exceptions import InvalidRelationshipTypeException


@dataclass(frozen=True)
class RelationshipType:
    name: str
    source_type: AssetType
    target_type: AssetType
    is_bidirectional: bool = False
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not (isinstance(self.source_type, AssetType)) or not (
            isinstance(self.target_type, AssetType)
        ):
            raise InvalidRelationshipTypeException

        if not isinstance(self.is_bidirectional, bool):
            raise InvalidRelationshipTypeException

    def __eq__(self, other) -> bool:
        if not isinstance(other, RelationshipType):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
