from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .controller import Controller

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = ["media_player"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    # Store an instance of the "connecting" class that does the work of speaking
    # with your actual devices.
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Controller(entry.data["host"])

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
