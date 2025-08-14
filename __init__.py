"""HTTP Action custom component."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from . import http_action

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HTTP Action component."""
    return await http_action.async_setup(hass, config)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HTTP Action from a config entry."""
    # No per-entry data needed; just register the service if not already registered
    if not hass.data.get("http_action_service_registered"):
        await http_action.async_setup(hass, {})
        hass.data["http_action_service_registered"] = True
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry for HTTP Action."""
    # Nothing to clean up, as the service is global
    return True
