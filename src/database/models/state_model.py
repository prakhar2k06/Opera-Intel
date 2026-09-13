from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel


class StateModel(Base):
    __tablename__ = "states"

    __table_args__ = (
        UniqueConstraint(
            "asset_type_id",
            "name",
            name="uq_states_asset_type_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(
        back_populates="states", foreign_keys=[asset_type_id]
    )
    name: Mapped[str]
