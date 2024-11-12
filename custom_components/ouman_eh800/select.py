import logging

from homeassistant.components.select import (
    SelectEntity,
    SelectEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN
from .eh800 import OPERATION_MODES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device climate control."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceSelect] = [
        OumanEH800DeviceSelect(
            device,
            SelectEntityDescription(
                key="l1_operation_mode",
            ),
        )
    ]

    async_add_entities(entities, True)


class OumanEH800DeviceSelect(SelectEntity):
    entity_description: SelectEntityDescription

    def __init__(
        self,
        device: OumanEH800Device,
        description: SelectEntityDescription,
    ) -> None:
        self._device = device
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def current_option(self) -> str:
        operation_mode = int(
            self._device.device.data.get(self.entity_description.key, 0)
        )
        return [om.name for om in OPERATION_MODES if om.value == operation_mode][0]

    @property
    def options(self) -> list[str]:
        return [om.name for om in OPERATION_MODES]

    async def async_select_option(self, option: str) -> None:
        operation_mode = [om for om in OPERATION_MODES if om.name == option][0]
        _LOGGER.debug(
            "Setting operation mode to '%s' (%s)",
            operation_mode.name,
            operation_mode.value,
        )
        await self._device.device.update_value(
            self.entity_description.key,
            operation_mode.value,
        )
        self.async_write_ha_state()

    async def async_update(self) -> None:
        await self._device.async_update()
