"""
TODO
"""

import logging

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
    TEMPERATURE_SENSOR_TYPE_L1_SUPPLY,
    TEMPERATURE_SENSOR_TYPE_L1_ROOM,
    TEMPERATURE_SENSOR_TYPE_OUTSIDE,
)
from .eh800 import EH800

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """TODO"""
    config = hass.data[DOMAIN][entry.entry_id]

    eh800 = EH800(
        config[CONF_HOST],
        config[CONF_PORT],
        config[CONF_USERNAME],
        config[CONF_PASSWORD],
    )

    entities = []
    entities.append(TemperatureSensor(hass, eh800, TEMPERATURE_SENSOR_TYPE_OUTSIDE))
    entities.append(TemperatureSensor(hass, eh800, TEMPERATURE_SENSOR_TYPE_L1_ROOM))
    entities.append(TemperatureSensor(hass, eh800, TEMPERATURE_SENSOR_TYPE_L1_SUPPLY))

    async_add_entities(entities)

    return True


class TemperatureSensor(SensorEntity):
    """Temperature sensor"""

    def __init__(self, hass: HomeAssistant, api: EH800, sensor_type: str):
        self._hass = hass
        self._api = api
        self._sensor_type = sensor_type

        self._unique_id = f"{DOMAIN}_temperature_{sensor_type}".lower()

        self._state = 0.0

    @property
    def device_class(self):
        """TODO"""
        return SensorDeviceClass.TEMPERATURE

    @property
    def device_info(self):
        """TODO"""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
        }

    @property
    def name(self):
        """TODO"""
        return self.unique_id

    @property
    def native_unit_of_measurement(self):
        """TODO"""
        return UnitOfTemperature.CELSIUS

    @property
    def state(self):
        """TODO"""
        return self._state

    @property
    def state_class(self):
        """TODO"""
        return SensorStateClass.MEASUREMENT

    @property
    def unique_id(self):
        """TODO"""
        return self._unique_id

    @Throttle(timedelta(minutes=1))
    async def async_update(self):
        """TODO"""
        if self._sensor_type == TEMPERATURE_SENSOR_TYPE_OUTSIDE:
            await self._hass.async_add_executor_job(self._api.update_outside_temp)
            self._state = self._api.get_outside_temp()
        elif self._sensor_type == TEMPERATURE_SENSOR_TYPE_L1_ROOM:
            await self._hass.async_add_executor_job(self._api.update_l1_room_temp)
            self._state = self._api.get_l1_room_temp()
        elif self._sensor_type == TEMPERATURE_SENSOR_TYPE_L1_SUPPLY:
            await self._hass.async_add_executor_job(self._api.update_l1_supply_temp)
            self._state = self._api.get_l1_supply_temp()
