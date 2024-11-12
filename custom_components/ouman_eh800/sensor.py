import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


TEMPERATURE_SENSORS: tuple[str, ...] = (
    "outside_temperature",
    "l1_supply_temperature",
    "l1_room_temperature",
    "l1_tmrsp",
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device sensors."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceSensor] = [
        OumanEH800DeviceSensor(
            device,
            sensor,
            SensorEntityDescription(
                key=sensor,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
            ),
        )
        for sensor in TEMPERATURE_SENSORS
    ]

    async_add_entities(entities, True)


class OumanEH800DeviceSensor(SensorEntity):
    entity_description: SensorEntityDescription

    def __init__(
        self,
        device: OumanEH800Device,
        value_key: str,
        description: SensorEntityDescription,
    ) -> None:
        self._device = device
        self._value_key = value_key
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def native_value(self) -> float:
        return self._device.device.data.get(self._value_key, 0.0)

    async def async_update(self) -> None:
        await self._device.async_update()
