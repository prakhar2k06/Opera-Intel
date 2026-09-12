from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.assets.property_type import PropertyType
from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel


class PropertyModel(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    name: Mapped[str]
    property_type: Mapped[PropertyType]
    required: Mapped[bool]
    default_value: Mapped[Any] = mapped_column(
        JSON,
        nullable=True,
    )
    asset_type: Mapped["AssetTypeModel"] = relationship(back_populates="properties")

    def __repr__(self) -> str:
        return f"Property({self.name}, {self.property_type})"
