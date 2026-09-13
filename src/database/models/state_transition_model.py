from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel
    from .state_model import StateModel


class StateTransitionModel(Base):
    __tablename__ = "state_transitions"

    __table_args__ = (
        UniqueConstraint(
            "asset_type_id",
            "source_state_id",
            "target_state_id",
            name="uq_state_transitions_asset_source_target",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(back_populates="transitions")
    source_state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    source_state: Mapped["StateModel"] = relationship(foreign_keys=[source_state_id])
    target_state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    target_state: Mapped["StateModel"] = relationship(foreign_keys=[target_state_id])

    def __repr__(self) -> str:
        return f"StateTransition({self.source_state_id} -> {self.target_state_id})"
