from homeassistant.components.sensor import SensorEntity
from homeassistant.const import POWER_WATT, PERCENTAGE
from .const import DOMAIN

SENSOR_TYPES = {
    "pv_power": ("PV-Erzeugung", POWER_WATT),
    "grid_export": ("Einspeisung", POWER_WATT),
    "grid_import": ("Bezug", POWER_WATT),
    "house_consumption": ("Hausverbrauch", POWER_WATT),
    "battery_soc": ("Batterie SOC", PERCENTAGE),
    "battery_charge": ("Batterie lädt", POWER_WATT),
    "battery_discharge": ("Batterie entlädt", POWER_WATT),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for key, (name, unit) in SENSOR_TYPES.items():
        entities.append(SenecSensor(coordinator, key, name, unit))
    async_add_entities(entities)

class SenecSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        self._coordinator = coordinator
        self._key = key
        self._name = name
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def unique_id(self):
        return f"mysenec_local_{self._key}"

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self._coordinator.async_request_refresh()