"""Config flow for HTTP Action custom component."""

from homeassistant import config_entries

from .const import DOMAIN


class HttpActionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HTTP Action."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="HTTP Action", data={})
        return self.async_show_form(
            step_id="user",
            data_schema=None,
            errors=errors,
        )
