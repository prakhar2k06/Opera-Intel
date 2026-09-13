from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_model import AssetModel
    from .relationship_type_model import RelationshipTypeModel


class RelationshipModel(Base):
    __tablename__ = "relationships"

    __table_args__ = (
        UniqueConstraint(
            "relationship_type_id",
            "source_asset_id",
            "target_asset_id",
            name="uq_relationship_type_source_target",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    relationship_type_id: Mapped[int] = mapped_column(
        ForeignKey("relationship_types.id")
    )
    relationship_type: Mapped["RelationshipTypeModel"] = relationship()
    source_asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    source_asset: Mapped["AssetModel"] = relationship(foreign_keys=[source_asset_id])
    target_asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    target_asset: Mapped["AssetModel"] = relationship(foreign_keys=[target_asset_id])
