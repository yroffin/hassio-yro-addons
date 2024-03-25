from dataclasses import dataclass
from collections.abc import Callable
from datetime import datetime, timedelta
import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.dt import now

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import StateType

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPower,
)

from .coordinator import BeemAppUpdateCoordinator

from .const import DOMAIN
from .entity import BeemEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up all sensors for this entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(BeemEntity(coordinator, description) for description in SENSORS)

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

        self.refreshState()

    @property
    def icon(self) -> str | None:
        return "mdi:heat-wave"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.serialNumber)},
            name="BeemBox",
            manufacturer="Beem",
            configuration_url="https://www.google.fr",
            serial_number=self.coordinator.serialNumber,
            model=DOMAIN
        )

    @property
    def unique_id(self) -> str:
        """Return the uuid as the unique_id."""
        return f"{self.coordinator.serialNumber}_{self.entity_description.key}"

    @property
    def available(self) -> bool:
        """Determine if the sensor is available based on API results."""
        return True

    @property
    def native_value(self) -> float | None:
        """Return the state, rounding off to reasonable values."""
        return 5.

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle coordinator update."""
        super()._handle_coordinator_update()

        self.refreshState()

    def refreshState(self) -> None:
        if self.entity_description.key:
             self._attr_state = self.coordinator.data[self.entity_description.key]
             _LOGGER.debug("refreshState: {} = {} / {}".format(self.entity_description.key,self._attr_state,self.coordinator.data))

@dataclass(frozen=True, kw_only=True)
class BeemSensorEntityDescription(SensorEntityDescription):
    """Describes a Beem sensor entity."""

SENSORS: tuple[BeemSensorEntityDescription, ...] = (
    BeemSensorEntityDescription(
        key="totalMonth",
        name = "totalMonth",
        translation_key="totalMonth",
        icon="mdi:solar-power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    BeemSensorEntityDescription(
        key="wattHour",
        name = "wattHour",
        translation_key="wattHour",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    BeemSensorEntityDescription(
        key="totalDay",
        name = "totalDay",
        translation_key="totalDay",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
    ),
)
