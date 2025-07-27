"""MySenec Local Integration."""

from .const import DOMAIN
from .senec_api import SenecLocalAPI
from .coordinator import MySenecDataUpdateCoordinator

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import discovery

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = SenecLocalAPI(entry.data["host"])
    coordinator = MySenecDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, platform)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True