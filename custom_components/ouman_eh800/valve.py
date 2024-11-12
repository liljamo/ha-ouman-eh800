import logging

from homeassistant.components.valve import (
    ValveDeviceClass,
    ValveEntity,
    ValveEntityDescription,
    ValveEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


VALVES_RO: tuple[str, ...] = ("l1_valve_position",)

VALVES_RW: tuple[str, ...] = ("l1_manual_drive_valve_position",)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device valves."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceValve] = []

    entities.extend(
        [
            OumanEH800DeviceValveRO(
                device,
                valve,
                ValveEntityDescription(
                    key=valve,
                    device_class=ValveDeviceClass.WATER,
                ),
            )
            for valve in VALVES_RO
        ]
    )

    entities.extend(
        [
            OumanEH800DeviceValveRW(
                device,
                valve,
                ValveEntityDescription(
                    key=valve,
                    device_class=ValveDeviceClass.WATER,
                ),
            )
            for valve in VALVES_RW
        ]
    )

    async_add_entities(entities, True)


class OumanEH800DeviceValve(ValveEntity):
    entity_description: ValveEntityDescription

    def __init__(
        self,
        device: OumanEH800Device,
        value_key: str,
        description: ValveEntityDescription,
    ) -> None:
        self._device = device
        self._value_key = value_key
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def current_valve_position(self) -> int:
        return int(self._device.device.data.get(self._value_key, 0))

    @property
    def reports_position(self) -> bool:
        return True

    async def async_update(self) -> None:
        await self._device.async_update()


class OumanEH800DeviceValveRO(OumanEH800DeviceValve):
    """A valve that can only be read."""


class OumanEH800DeviceValveRW(OumanEH800DeviceValve):
    """
    A valve that can be read and set.

    Supports setting the position of the valve, and closing the valve.
    """

    _attr_supported_features = (
        ValveEntityFeature.CLOSE | ValveEntityFeature.SET_POSITION
    )

    async def async_set_valve_position(self, position: int) -> None:
        await self._device.device.update_value(self.entity_description.key, position)
        self.async_write_ha_state()
