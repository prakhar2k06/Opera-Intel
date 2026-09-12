from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel


class StateModel(Base):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    name: Mapped[str]
    asset_type: Mapped["AssetTypeModel"] = relationship(
        back_populates="states",
        foreign_keys=[asset_type_id],
    )

    def __repr__(self) -> str:
        return f"State({self.name})"
