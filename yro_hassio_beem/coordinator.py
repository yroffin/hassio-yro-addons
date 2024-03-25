"""Contains the shared Coordinator for Beem systems."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BeemAppApiClient, BeemAppData

_LOGGER = logging.getLogger(__name__)

class BeemAppUpdateCoordinator(DataUpdateCoordinator):
    """Coordinates updates between all entries defined in this file."""

    def __repr__(self): 
        return "BeemAppUpdateCoordinator {} => {}".format(self.name, self.data)

    def __init__(self, hass: HomeAssistant, name: str, serialNumber: str) -> None:
        """Initialize an UpdateCoordinator for a group of sensors."""

        super().__init__(
            hass,
            logger=_LOGGER,
            name=name,
            update_interval=timedelta(seconds=30),
        )

        self.login = None
        self.serialNumber = serialNumber
        self.data = {
            "serialNumber": serialNumber,
            "accessToken": None
        }

        # load initial data
        self.async_update_data()

    async def _async_update_data(self) -> BeemAppData:
        async with asyncio.timeout(5):
            return await self.async_update_data()

    async def async_update_data(self) -> BeemAppData:
        try:
            if "accessToken" not in self.data or self.data["accessToken"] == None:
                login = await BeemAppApiClient.postLogin(self.hass)
                self.data["accessToken"] = login.login['accessToken']
        except Exception as exc:

            try:
                if "accessToken" not in self.data or self.data["accessToken"] == None:
                    login = await BeemAppApiClient.postLogin(self.hass)
                    self.data["accessToken"] = login.login['accessToken']
            except Exception as exc:
                _LOGGER.error("Error while login to api %s", exc)
                raise UpdateFailed from exc

        try:
            # call api
            data = await BeemAppApiClient.postSummary(self.hass, self.data["accessToken"])
            # update surrent state
            for summary in data.summary:
                if summary["serialNumber"] == self.data["serialNumber"]:
                    return {
                        "serialNumber": self.data["serialNumber"],
                        "totalMonth": summary["totalMonth"],
                        "wattHour": summary["wattHour"],
                        "totalDay": summary["totalDay"],
                        "accessToken": self.data["accessToken"],
                    }
            return None
        except Exception as exc:
            _LOGGER.error("Error while getting summary %s", exc)
            self.data["accessToken"] = None
            raise UpdateFailed from exc
