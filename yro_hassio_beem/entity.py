"""Contains base entity classes for Beem entities."""

from dataclasses import dataclass

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import BeemAppUpdateCoordinator

from homeassistant.components.sensor import (
    SensorDeviceClass,
)

class BeemEntity(CoordinatorEntity[BeemAppUpdateCoordinator], Entity):
    """A base entity that is registered under a Beem device."""

    def __init__(
        self, coordinator: BeemAppUpdateCoordinator, description: EntityDescription
    ) -> None:
        """Initialize the device info and set the update coordinator."""
        super().__init__(coordinator)

        self.box = coordinator.data

        self._attr_unique_id = f"{self.coordinator.serialNumber}_{description.key}"
        self.entity_description = description

    @property
    def icon(self) -> str | None:
        return "mdi:solar-power"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.box["serialNumber"])},
            name="BeemBox",
            manufacturer="Beem",
            configuration_url="https://www.google.fr",
            serial_number=self.box["serialNumber"],
            model=DOMAIN
        )

    @property
    def state_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.ENERGY
