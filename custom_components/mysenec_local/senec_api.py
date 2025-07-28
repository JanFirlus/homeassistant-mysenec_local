import aiohttp
import ssl
import logging

_LOGGER = logging.getLogger(__name__)

class SenecLocalAPI:
    def __init__(self, host):
        self._url = f"https://{host}/lala.cgi"
        _LOGGER.debug("Verwende SENEC-URL: %s", self._url)

    async def async_get_data(self):
        payload = {
            "STATISTIC": {
                "LIVE_GRID_IMPORT": "",
                "LIVE_GRID_EXPORT": "",
                "LIVE_HOUSE_CONSUMPTION": "",
                "LIVE_PV_GEN": "",
                "LIVE_BAT_CHARGE": "",
                "LIVE_BAT_DISCHARGE": "",
                "LIVE_BAT_SOC": ""
            }
        }

        sslcontext = ssl._create_unverified_context()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self._url, json=payload, timeout=5, ssl=sslcontext) as resp:
                    result = await resp.json()
                    data = result["STATISTIC"]
                    return {
                        "grid_import": data["LIVE_GRID_IMPORT"],
                        "grid_export": data["LIVE_GRID_EXPORT"],
                        "house_consumption": data["LIVE_HOUSE_CONSUMPTION"],
                        "pv_power": data["LIVE_PV_GEN"],
                        "battery_charge": data["LIVE_BAT_CHARGE"],
                        "battery_discharge": data["LIVE_BAT_DISCHARGE"],
                        "battery_soc": data["LIVE_BAT_SOC"]
                    }
        except Exception as e:
            _LOGGER.error("SENEC API Fehler: %s", e)
            return {}
