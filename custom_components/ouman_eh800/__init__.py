from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import Throttle

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
from .eh800 import EH800

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CLIMATE, Platform.NUMBER, Platform.SENSOR, Platform.VALVE]

UPDATE_INTERVAL = timedelta(minutes=1)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Setting up Ouman EH-800")

    config = dict(entry.data)
    eh800 = EH800(
        config[CONF_HOST],
        config[CONF_PORT],
        config[CONF_USERNAME],
        config[CONF_PASSWORD],
    )
    # Do an initial update straight away.
    await eh800.update()

    device = OumanEH800Device(hass, eh800, entry)

    hass.data.setdefault(DOMAIN, {}).update({entry.entry_id: device})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


class OumanEH800Device:
    """Ouman EH-800 Device instance."""

    def __init__(self, hass: HomeAssistant, device: EH800, entry: ConfigEntry) -> None:
        self._hass = hass
        self.device = device
        self.entry = entry

    @Throttle(UPDATE_INTERVAL)
    async def async_update(
        self,
        **kwargs,  # pylint: disable=unused-argument
    ):
        """Pull data from Ouman EH-800."""

        update_ok = await self.device.update()
        if not update_ok:
            _LOGGER.warning("Failed to update EH-800 device!")

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            manufacturer="Ouman",
            name="Ouman EH-800",
        )
