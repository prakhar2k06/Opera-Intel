from ...domain.assets.property import Property
from ...domain.assets.sentinel import Sentinel
from ..models.property_model import PropertyModel


class PropertyMapper:
    def to_model(self, property: Property) -> PropertyModel:
        has_default: bool = property.default_value is not Sentinel.UNDEFINED
        return PropertyModel(
            name=property.name,
            property_type=property.property_type,
            required=property.required,
            has_default=has_default,
            default_value=property.default_value if has_default else None,
        )

    def to_domain(self, property_model: PropertyModel) -> Property:
        return Property(
            name=property_model.name,
            property_type=property_model.property_type,
            required=property_model.required,
            default_value=(
                property_model.default_value
                if property_model.has_default
                else Sentinel.UNDEFINED
            ),
        )
