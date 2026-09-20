from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel
    from .state_model import StateModel


class RuleModel(Base):
    __tablename__ = "rules"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    asset_type_id: Mapped[UUID] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(
        back_populates="rules", foreign_keys=[asset_type_id]
    )
    trigger: Mapped[str]
    condition: Mapped[dict[str, Any]] = mapped_column(JSONB)
    target_state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    target_state: Mapped["StateModel"] = relationship(foreign_keys=[target_state_id])
