"""Config flow for BeemApp."""

from __future__ import annotations

import logging
import requests
import os

from typing import Any

import voluptuous as vol
from homeassistant.helpers import config_validation as cv, selector

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_IP_ADDRESS

from .api import BeemAppApiClient, BeemAppData

from .const import DATA_CREDS, DATA_CREDS_PASSWORD, DATA_CREDS_USERNAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BeemAppConfigFlow(ConfigFlow, domain=DOMAIN):
    """The configuration flow for a BeemApp system."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 2
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        """Ask the user information on its beem system."""

        _LOGGER.warn("async_step_user".format())

        login_data = await BeemAppApiClient.postLogin(self.hass)
        summary_data: BeemAppData = None

        if login_data:
            summary_data = await BeemAppApiClient.postSummary(
                self.hass,
                accessToken=login_data.login["accessToken"]
            )

        if user_input and user_input["box"]:
            # Make sure we're not configuring the same device
            uid = user_input["box"]
            await self.async_set_unique_id(uid)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Beem",
                data=user_input
            )
        else:
            # check if device is loaded
            if login_data and summary_data:
                all_devices = {}
                for box in summary_data.summary:
                    all_devices[box["serialNumber"]] = "Associate box {}".format(
                        box["serialNumber"]
                    )

                # https://alecthomas.github.io/voluptuous/docs/_build/html/index.html
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Required(
                                "box", default=list(all_devices.keys())[0]
                            ): selector.SelectSelector(
                                selector.SelectSelectorConfig(
                                    options=list(all_devices.keys()),
                                    translation_key="thermostat_type",
                                    mode="list",
                                )
                            )
                        }
                    ),
                    errors={},
                )
            else:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Optional("box", default=list([])): cv.multi_select([]),
                        }
                    ),
                    errors={
                        "box": "Cannot connect to this box with account {}, check your configuration".format(
                            self.hass.data[DOMAIN][DATA_CREDS][DATA_CREDS_USERNAME]
                        )
                    },
                )
