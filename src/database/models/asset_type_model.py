from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .property_model import PropertyModel
    from .state_model import StateModel
    from .state_transition_model import StateTransitionModel


class AssetTypeModel(Base):
    __tablename__ = "asset_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_published: Mapped[bool]
    initial_state_id: Mapped[int | None] = mapped_column(
        ForeignKey("states.id"),
        nullable=True,
    )
    properties: Mapped[list["PropertyModel"]] = relationship(
        back_populates="asset_type",
    )
    states: Mapped[list["StateModel"]] = relationship(
        back_populates="asset_type",
        foreign_keys="StateModel.asset_type_id",
    )
    transitions: Mapped[list["StateTransitionModel"]] = relationship(
        back_populates="asset_type",
    )
    initial_state: Mapped["StateModel | None"] = relationship(
        foreign_keys=[initial_state_id],
        post_update=True,
    )

    def __repr__(self) -> str:
        return f"AssetType({self.name})"
