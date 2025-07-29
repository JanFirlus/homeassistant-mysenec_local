import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfPower, PERCENTAGE
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "pv_power": ("PV-Erzeugung", UnitOfPower),
    "grid_export": ("Einspeisung", UnitOfPower),
    "grid_import": ("Bezug", UnitOfPower),
    "house_consumption": ("Hausverbrauch", UnitOfPower),
    "battery_soc": ("Batterie SOC", PERCENTAGE),
    "battery_charge": ("Batterie lädt", UnitOfPower),
    "battery_discharge": ("Batterie entlädt", UnitOfPower),
}

async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.debug("Starte Sensor-Setup für MySenec Local...")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, (name, unit) in SENSOR_TYPES.items():
        entities.append(SenecSensor(coordinator, key, name, unit))
        _LOGGER.debug("Sensor erstellt: %s", key)

    async_add_entities(entities)
    _LOGGER.debug("Alle Sensoren registriert.")

class SenecSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        self._coordinator = coordinator
        self._key = key
        self._name = name
        self._unit = unit
        self._attr_should_poll = False

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
    def state(self):
        if not self._coordinator.data:
            _LOGGER.warning("Keine Daten im Coordinator für %s", self._key)
            return None
        value = self._coordinator.data.get(self._key)
        _LOGGER.debug("Sensor %s Wert: %s", self._key, value)
        return value

    async def async_update(self):
        await self._coordinator.async_request_refresh()
