from dataclasses import dataclass

from .property_type import PropertyType
from .sentinel import Sentinel


@dataclass(frozen=True)
class Property:
    name: str
    property_type: PropertyType
    required: bool
    default_value: object | Sentinel = Sentinel.UNDEFINED
