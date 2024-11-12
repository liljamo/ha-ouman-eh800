import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityDescription,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import OumanEH800Device
from .const import DOMAIN
from .eh800 import OPERATION_MODES

_LOGGER = logging.getLogger(__name__)


class OumanEH800DeviceClimateEntityDescription(
    ClimateEntityDescription, frozen_or_thawed=True
):  # pylint: disable=too-few-public-methods
    current_temperature_key: str
    target_temperature_key: str
    operation_mode_key: str


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Ouman EH-800 device climate control."""
    device = hass.data[DOMAIN].get(entry.entry_id)

    entities: list[OumanEH800DeviceClimate] = [
        OumanEH800DeviceClimate(
            device,
            OumanEH800DeviceClimateEntityDescription(
                key="l1_climate",
                current_temperature_key="l1_room_temperature",
                target_temperature_key="l1_target_room_temperature",
                operation_mode_key="l1_operation_mode",
            ),
        )
    ]

    async_add_entities(entities, True)


class OumanEH800DeviceClimate(ClimateEntity):
    entity_description: OumanEH800DeviceClimateEntityDescription

    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        device: OumanEH800Device,
        description: OumanEH800DeviceClimateEntityDescription,
    ) -> None:
        self._device = device
        self.entity_description = description

        self._attr_name = description.key.replace("_", " ").capitalize()
        self._attr_unique_id = f"ouman_eh800_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def extra_state_attributes(self) -> dict:
        return self._device.device.data

    @property
    def hvac_mode(self) -> HVACMode:
        operation_mode = int(
            self._device.device.data.get(self.entity_description.operation_mode_key, 0)
        )
        if operation_mode == 5:
            return HVACMode.OFF
        if operation_mode == 0:
            return HVACMode.AUTO
        return HVACMode.HEAT

    @property
    def hvac_modes(self) -> list[HVACMode]:
        return []

    @property
    def preset_mode(self) -> str:
        operation_mode = int(
            self._device.device.data.get(self.entity_description.operation_mode_key, 0)
        )
        return [om.name for om in OPERATION_MODES if om.value == operation_mode][0]

    @property
    def preset_modes(self) -> list[str]:
        return [om.name for om in OPERATION_MODES]

    @property
    def current_temperature(self) -> float:
        return float(
            self._device.device.data.get(
                self.entity_description.current_temperature_key, 0.0
            )
        )

    @property
    def target_temperature(self) -> float:
        return float(
            self._device.device.data.get(
                self.entity_description.target_temperature_key, 0.0
            )
        )

    async def async_set_temperature(self, **kwargs) -> None:
        await self._device.device.update_value(
            self.entity_description.target_temperature_key,
            kwargs.get("temperature", self.target_temperature),
        )
        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        operation_mode = [om for om in OPERATION_MODES if om.name == preset_mode][0]
        _LOGGER.debug(
            "Setting operation mode to '%s' (%s)",
            operation_mode.name,
            operation_mode.value,
        )
        await self._device.device.update_value(
            self.entity_description.operation_mode_key,
            operation_mode.value,
        )
        self.async_write_ha_state()

    async def async_update(self) -> None:
        await self._device.async_update()
