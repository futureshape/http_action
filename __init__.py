"""HTTP Action custom component."""

import logging

from homeassistant.core import HomeAssistant

from . import http_action

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant | None, config):
    """Set up the HTTP Action component."""
    return await http_action.async_setup(hass, config)
