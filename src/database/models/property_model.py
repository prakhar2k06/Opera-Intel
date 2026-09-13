from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...domain.assets.property_type import PropertyType
from .base import Base

if TYPE_CHECKING:
    from .asset_type_model import AssetTypeModel


class PropertyModel(Base):
    __tablename__ = "properties"

    __table_args__ = (
        UniqueConstraint(
            "asset_type_id",
            "name",
            name="uq_properties_asset_type_name",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type_id: Mapped[int] = mapped_column(ForeignKey("asset_types.id"))
    asset_type: Mapped["AssetTypeModel"] = relationship(back_populates="properties")
    name: Mapped[str]
    property_type: Mapped[PropertyType]
    required: Mapped[bool]
    default_value: Mapped[Any] = mapped_column(
        JSON,
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"Property({self.name}, {self.property_type})"
