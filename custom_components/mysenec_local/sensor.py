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
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"mysenec_local_{key}"
        self._attr_should_poll = False

    @property
    def available(self):
        return self._coordinator.last_update_success

    @property
    def native_value(self):
        return self._coordinator.data.get(self._key)

    @property
    def device_class(self):
        if self._key == "battery_soc":
            return "battery"
        return "power"


    async def async_update(self):
        await self._coordinator.async_request_refresh()