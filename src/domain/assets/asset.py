from uuid import UUID, uuid4

from src.domain.assets.property import Property

from ..events.asset_property_changed_event import AssetPropertyChangedEvent
from ..events.asset_state_changed_event import AssetStateChangedEvent
from ..events.domain_event import DomainEvent
from .asset_type import AssetType
from .exceptions import (
    InvalidAssetStateTransitionException,
    InvalidPropertyValueException,
    InvalidTargetStateException,
    MissingPropertyException,
    UnknownPropertyException,
    UnpublishedAssetTypeException,
)
from .sentinel import Sentinel
from .state import State


class Asset:
    def __init__(
        self, name: str, asset_type: AssetType, properties: dict, id: UUID | None = None
    ) -> None:
        if not asset_type.is_published:
            raise UnpublishedAssetTypeException

        self.id: UUID = id if id is not None else uuid4()
        self.name: str = name
        self.asset_type: AssetType = asset_type
        self.properties: dict = {}
        self.current_state: State | None = asset_type.initial_state
        self._domain_events: list[DomainEvent] = []

        for property_name in properties:
            if property_name not in self.asset_type.properties:
                raise UnknownPropertyException

        for property_name, property_definition in self.asset_type.properties.items():
            if property_name in properties:
                value = properties[property_name]

                if not property_definition.property_type.validate(value):
                    raise InvalidPropertyValueException

                self.properties[property_name] = value

            elif property_definition.default_value is not Sentinel.UNDEFINED:
                if not property_definition.property_type.validate(
                    property_definition.default_value
                ):
                    raise InvalidPropertyValueException

                self.properties[property_name] = property_definition.default_value

            elif property_definition.required:
                raise MissingPropertyException

            else:
                self.properties[property_name] = None

    def __eq__(self, other) -> bool:
        if not isinstance(other, Asset):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def transition(self, target: State) -> None:
        if not isinstance(target, State):
            raise InvalidTargetStateException

        if self.current_state is None:
            raise InvalidAssetStateTransitionException

        if target not in self.asset_type.states:
            raise InvalidTargetStateException

        if not self.asset_type.can_transition(self.current_state, target):
            raise InvalidAssetStateTransitionException

        previous_state: State = self.current_state
        self.current_state = target

        self._domain_events.append(
            AssetStateChangedEvent(
                asset=self, previous_state=previous_state, new_state=target
            )
        )

    def update_property(self, property_name: str, new_value) -> None:
        if property_name not in self.asset_type.properties:
            raise UnknownPropertyException

        property_definition: Property = self.asset_type.properties[property_name]

        if not property_definition.property_type.validate(new_value):
            raise InvalidPropertyValueException

        previous_value = self.properties[property_name]

        if previous_value == new_value:
            return

        self.properties[property_name] = new_value

        self._domain_events.append(
            AssetPropertyChangedEvent(
                asset=self,
                property=property_definition,
                previous_value=previous_value,
                new_value=new_value,
            )
        )

    def pull_domain_events(self) -> list:
        events: list[DomainEvent] = list(self._domain_events)
        self._domain_events.clear()
        return events

    @classmethod
    def reconstruct_asset(
        cls,
        id: UUID,
        asset_type: AssetType,
        name: str,
        properties: dict,
        current_state: State | None,
    ) -> "Asset":
        asset = cls(
            id=id,
            asset_type=asset_type,
            name=name,
            properties=properties,
        )

        if current_state and current_state not in asset_type.states:
            raise InvalidTargetStateException

        asset.current_state = current_state
        asset._domain_events = []

        return asset
