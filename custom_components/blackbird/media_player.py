from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerDeviceClass
from homeassistant.components.media_player.const import MEDIA_TYPE_CHANNEL, SUPPORT_SELECT_SOURCE, SUPPORT_TURN_ON, \
    SUPPORT_TURN_OFF, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_STEP
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .controller import Controller


# This function is called as part of the __init__.async_setup_entry (via the
# hass.config_entries.async_forward_entry_setup call)
async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add media_player for passed config_entry in HA."""
    # The hub is loaded from the associated hass.data entry that was created in the
    # __init__.async_setup_entry function

    controller = Controller(entry.data.get("host"))
    await controller.refresh()
    async_add_entities([BlackbirdMediaPlayer(controller, controller.id, controller.name)])


# noinspection PyAbstractClass
class BlackbirdMediaPlayer(MediaPlayerEntity):
    _attr_media_content_type = MEDIA_TYPE_CHANNEL
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = SUPPORT_SELECT_SOURCE | SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_STEP

    _attr_should_poll = True

    def __init__(self, controller: Controller, unique_id, name) -> None:
        self._controller = controller

        self._attr_unique_id = unique_id
        self._attr_name = name
        self._available = True

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            "name": self.name
        }

    @property
    def source(self) -> str:
        return self._controller.current_input

    @property
    def source_list(self) -> list[str]:
        return self._controller.input_sources

    @property
    def state(self) -> str:
        return self.source

    @property
    def available(self) -> bool:
        return self._available

    async def async_turn_on(self):
        await self._controller.turn_on_display()

    async def async_turn_off(self):
        await self._controller.turn_off_display()

    async def async_mute_volume(self, mute):
        await self._controller.mute_volume()

    async def async_volume_up(self):
        await self._controller.increase_volume()

    async def async_volume_down(self):
        await self._controller.decrease_volume()

    async def async_select_source(self, source):
        await self._controller.set_input(source)

    async def async_update(self):
        await self._controller.refresh()
