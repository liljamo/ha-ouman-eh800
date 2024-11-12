import logging

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device sensors."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceHomeAwaySwitch] = [
        OumanEH800DeviceHomeAwaySwitch(
            device,
            SwitchEntityDescription(
                key="home_away",
                device_class=SwitchDeviceClass.SWITCH,
            ),
        )
    ]

    async_add_entities(entities, True)


class OumanEH800DeviceHomeAwaySwitch(SwitchEntity):
    entity_description: SwitchEntityDescription

    def __init__(
        self,
        device: OumanEH800Device,
        description: SwitchEntityDescription,
    ) -> None:
        self._device = device
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def is_on(self) -> bool:
        value = int(self._device.device.data.get(self.entity_description.key))
        if value > 0:
            return False
        return True

    async def async_turn_off(
        self,
        **kwargs,  # pylint: disable=unused-argument
    ):
        await self._device.device.update_value(self.entity_description.key, 1)
        self.async_write_ha_state()

    async def async_turn_on(
        self,
        **kwargs,  # pylint: disable=unused-argument
    ):
        await self._device.device.update_value(self.entity_description.key, 0)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        await self._device.async_update()
