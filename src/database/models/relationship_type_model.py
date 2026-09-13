from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel


class RelationshipTypeModel(Base):
    __tablename__ = "relationship_types"

    __table_args__ = UniqueConstraint(
        "name",
        "source_asset_type_id",
        "target_asset_type_id",
        name="uq_relationship_type_name_source_target",
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    source_asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    source_asset_type: Mapped["AssetTypeModel"] = relationship(
        foreign_keys=[source_asset_type_id]
    )
    target_asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    target_asset_type: Mapped["AssetTypeModel"] = relationship(
        foreign_keys=[target_asset_type_id]
    )
    is_bidirectional: Mapped[bool]
