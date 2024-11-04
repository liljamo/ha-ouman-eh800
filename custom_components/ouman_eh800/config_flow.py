"""Ouman EH-800 config flow"""

import logging

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class OumanEH800ConfigFlow(
    ConfigFlow, domain=DOMAIN
):  # pylint: disable=too-few-public-methods
    """Ouman EH-800 config flow"""

    VERSION = 1

    async def _create_entry(
        self, host: str, port: int, username: str, password: str
    ) -> ConfigFlowResult:
        """Register new entry."""
        return self.async_create_entry(
            title=f"Ouman {host}",
            data={
                CONF_HOST: host,
                CONF_PORT: port,
                CONF_USERNAME: username,
                CONF_PASSWORD: password,
            },
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """TODO"""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=USER_SCHEMA)

        _LOGGER.debug(user_input)
        return await self._create_entry(
            user_input[CONF_HOST],
            user_input[CONF_PORT],
            user_input[CONF_USERNAME],
            user_input[CONF_PASSWORD],
        )
