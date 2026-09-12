from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .asset_type_model import AssetTypeModel
from .base import Base


class StateModel(Base):
    __tablename__ = "states"
    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(back_populates="states")
    name: Mapped[str]
