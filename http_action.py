"""HTTP Action platform logic."""

import logging

import httpx
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.httpx_client import get_async_client

_LOGGER = logging.getLogger(__name__)

SERVICE_MAKE_REQUEST = "make_request"

MAKE_REQUEST_SCHEMA = vol.Schema(
    {
        vol.Required("method"): vol.In(["GET", "POST"]),
        vol.Required("url"): cv.string,
        vol.Optional("params"): dict,
        vol.Optional("data"): dict,  # for JSON
        vol.Optional("body"): cv.string,  # for arbitrary body
        vol.Optional("headers"): dict,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HTTP Action platform."""

    async def handle_make_request(call: ServiceCall) -> ServiceResponse:
        method = call.data["method"].upper()
        url = call.data["url"]
        params = call.data.get("params")
        data = call.data.get("data")
        body = call.data.get("body")
        headers = call.data.get("headers")
        try:
            async with get_async_client(hass) as client:
                if method == "GET":
                    resp = await client.get(url, params=params, headers=headers)
                elif method == "POST":
                    # Prefer 'body' if provided, else 'data' as JSON
                    if body is not None:
                        resp = await client.post(
                            url, params=params, content=body, headers=headers
                        )
                    elif data is not None:
                        resp = await client.post(
                            url, params=params, json=data, headers=headers
                        )
                    else:
                        resp = await client.post(url, params=params, headers=headers)
                else:
                    return {"error": f"Unsupported method: {method}"}
            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "body": resp.text,
            }
        except httpx.RequestError as ex:
            _LOGGER.error("HTTP request failed: %s", ex)
            return {"error": str(ex)}

    hass.services.async_register(
        "http_action",
        SERVICE_MAKE_REQUEST,
        handle_make_request,
        schema=MAKE_REQUEST_SCHEMA,
        supports_response=True,
    )
    return True
