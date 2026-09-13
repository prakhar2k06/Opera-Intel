from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey
from sqlalchemy.dialects import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel
    from .state_model import StateModel


class AssetModel(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(foreign_keys=[asset_type_id])
    name: Mapped[str]
    current_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id"), nullable=True
    )
    current_state: Mapped["StateModel | None"] = relationship(
        foreign_keys=[current_state_id], nullable=True
    )
    properties: Mapped[Any] = mapped_column(JSONB)
