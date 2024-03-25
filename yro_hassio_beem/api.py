"""Contains the shared api client for Beem systems."""

from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
import logging

from homeassistant.core import HomeAssistant
from .const import DATA_CREDS, DATA_CREDS_PASSWORD, DATA_CREDS_USERNAME, DOMAIN

import requests

_LOGGER = logging.getLogger(__name__)


@dataclass
class BeemAppData:
    """Contains data pulled from the Beem system."""

    def __repr__(self): 
        return "BeemAppDat login: {} list: {} summary: {}".format(self.login,self.list,self.summary)

    def __init__(self, login = None, list = None, summary = None) -> None:
        """Initialize data."""

        self.login = login
        self.list = list
        self.summary = summary

class BeemAppApiClient():
    """Api beem app client."""

    def __init__(self) -> None:
        """Initialize an BeemAppApiClient."""

        self.login = None

    async def postLogin(hass: HomeAssistant) -> BeemAppData:
        """Call login API."""

        result = await hass.async_add_executor_job(
            BeemAppApiClient.syncPostLogin,
            {
                "email": hass.data[DOMAIN][DATA_CREDS][DATA_CREDS_USERNAME],
                "password": hass.data[DOMAIN][DATA_CREDS][DATA_CREDS_PASSWORD],
            },
        )

        return result

    async def postSummary(hass: HomeAssistant, accessToken: str) -> BeemAppData:
        """Call box summary API."""

        result = await hass.async_add_executor_job(
            BeemAppApiClient.syncPostSummary,
            {
                "accessToken": accessToken,
            },
        )

        return result

    async def getBoxList(hass: HomeAssistant, accessToken: str) -> BeemAppData:
        """Call box summary API."""

        result = await hass.async_add_executor_job(
            BeemAppApiClient.syncGetBoxList,
            {
                "accessToken": accessToken,
            },
        )

        return result

    def syncPostLogin(
        args: None, url="https://api-x.beem.energy/beemapp/user/login"
    ) -> dict:
        """Post login on beem api with the given URL."""

        # Prepare the data you want to send as a dictionary
        data = {"email": args["email"], "password": args["password"]}

        # Send the POST request using the requests library
        response = requests.post(url, data=data)

        # Check the status code of the response to see if it was successful
        if response.status_code == 201:
            _LOGGER.debug("POST 201 - {}".format(url))
            return BeemAppData(login = response.json())
        else:
            _LOGGER.warn("POST - {} => {}: {}".format(url,response.status_code,response))
            # some error
            raise Exception(
                {"error": {"code": response.status_code, "text": response.text}}
            )

    def syncGetBoxList(
        args: None, url="https://api-x.beem.energy/beemapp/box/list"
    ) -> dict:
        """Get box list on beem api with the given URL."""

        # Send the GET request using the requests library
        response = requests.get(
            url, headers={"Authorization": "Bearer {}".format(args["accessToken"])}
        )

        # Check the status code of the response to see if it was successful
        if response.status_code == 200:
            return BeemAppData(list = response.json())
        else:
            _LOGGER.warn("GET - {} => {}: {}".format(url,response.status_code,response))
            # some error
            raise Exception(
                {"error": {"code": response.status_code, "text": response.text}}
            )

    def syncPostSummary(
        args: None, url="https://api-x.beem.energy/beemapp/box/summary"
    ) -> dict:
        """Get box summary on beem api with the given URL."""

        # get sysdate
        now = datetime.now()

        # Send the GET request using the requests library
        response = requests.post(
            url,
            headers={
                "content-type": "application/json",
                "authorization": "Bearer {}".format(args["accessToken"])
            },
            json = {
                "month": now.month,
                "year": now.year
            }
        )

        # Check the status code of the response to see if it was successful
        if response.status_code == 201:
            return BeemAppData(summary = response.json())
        else:
            _LOGGER.warn("POST - {} => {}: {}".format(url,response.status_code,response))
            # some error
            raise Exception(
                {"error": {"code": response.status_code, "text": response.text}}
            )
