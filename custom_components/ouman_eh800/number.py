import logging

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


NUMBERS: tuple[str, ...] = (
    "l1_temperature_drop",
    "l1_temperature_drop_big",
)
NUMBERS: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="l1_temperature_drop",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode="box",
        native_max_value=90.0,
        native_min_value=0.0,
        native_step=0.5,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    NumberEntityDescription(
        key="l1_temperature_drop_big",
        device_class=NumberDeviceClass.TEMPERATURE,
        mode="box",
        native_max_value=90.0,
        native_min_value=0.0,
        native_step=0.5,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device numbers."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceNumber] = [
        OumanEH800DeviceNumber(device, description) for description in NUMBERS
    ]

    async_add_entities(entities, True)


class OumanEH800DeviceNumber(NumberEntity):
    entity_description: NumberEntityDescription

    def __init__(
        self, device: OumanEH800Device, description: NumberEntityDescription
    ) -> None:
        self._device = device
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def native_value(self) -> float:
        return self._device.device.data.get(self.entity_description.key, 0.0)

    async def async_set_native_value(self, value: float) -> None:
        await self._device.device.update_value(self.entity_description.key, value)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        await self._device.async_update()
