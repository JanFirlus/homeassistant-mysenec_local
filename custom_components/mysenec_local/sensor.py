from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    POWER_WATT,
    PERCENTAGE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_BATTERY,
    STATE_CLASS_MEASUREMENT,
)
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "pv_power": ("PV-Erzeugung", POWER_WATT, DEVICE_CLASS_POWER),
    "grid_export": ("Einspeisung", POWER_WATT, DEVICE_CLASS_POWER),
    "grid_import": ("Bezug", POWER_WATT, DEVICE_CLASS_POWER),
    "house_consumption": ("Hausverbrauch", POWER_WATT, DEVICE_CLASS_POWER),
    "battery_soc": ("Batterie SOC", PERCENTAGE, DEVICE_CLASS_BATTERY),
    "battery_charge": ("Batterie lädt", POWER_WATT, DEVICE_CLASS_POWER),
    "battery_discharge": ("Batterie entlädt", POWER_WATT, DEVICE_CLASS_POWER),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, (name, unit, device_class) in SENSOR_TYPES.items():
        entities.append(SenecSensor(coordinator, key, name, unit, device_class))

    async_add_entities(entities, update_before_add=True)

class SenecSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit, device_class):
        self._coordinator = coordinator
        self._key = key
        self._name = name
        self._unit = unit
        self._device_class = device_class

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"mysenec_local_{self._key}"

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def native_value(self):
        value = self._coordinator.data.get(self._key)
        _LOGGER.debug("Sensor %s hat Wert: %s", self._key, value)
        return value

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT

    @property
    def device_class(self):
        return self._device_class

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self._coordinator.async_request_refresh()
