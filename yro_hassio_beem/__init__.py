"""The Beem integration."""

from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .coordinator import BeemAppUpdateCoordinator

from .const import DATA_CREDS, DATA_CREDS_USERNAME, DATA_CREDS_PASSWORD, DOMAIN

PLATFORMS = [
    Platform.SENSOR,
]

_LOGGER = logging.getLogger(__name__)

# https://alecthomas.github.io/voluptuous/docs/_build/html/index.html
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the beem component."""

    hass.data[DOMAIN] = {
        DATA_CREDS: {
            DATA_CREDS_USERNAME: config[DOMAIN].get(CONF_USERNAME),
            DATA_CREDS_PASSWORD: config[DOMAIN].get(CONF_PASSWORD),
        }
    }

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Beem from a config entry."""

    coordinator = BeemAppUpdateCoordinator(
        hass=hass,
        name=entry.title,
        serialNumber = entry.unique_id
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
