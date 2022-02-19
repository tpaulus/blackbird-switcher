from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerDeviceClass
from homeassistant.components.media_player.const import MEDIA_TYPE_CHANNEL, SUPPORT_SELECT_SOURCE, SUPPORT_TURN_ON, \
    SUPPORT_TURN_OFF, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_STEP, DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .controller import Controller


# This function is called as part of the __init__.async_setup_entry (via the
# hass.config_entries.async_forward_entry_setup call)
async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add media_player for passed config_entry in HA."""
    # The hub is loaded from the associated hass.data entry that was created in the
    # __init__.async_setup_entry function
    controller = hass.data[DOMAIN][config_entry.entry_id]

    # Add all entities to HA
    async_add_entities([controller])


# noinspection PyAbstractClass
class BlackbirdMediaPlayer(MediaPlayerEntity):
    _attr_media_content_type = MEDIA_TYPE_CHANNEL
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = SUPPORT_SELECT_SOURCE | SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_STEP

    _attr_should_poll = True

    def __init__(self, controller: Controller) -> None:
        self._controller = controller

        self._attr_unique_id = self._controller.id
        self._attr_name = self._controller.name

    def turn_on(self):
        self._controller.turn_on_display()

    def turn_off(self):
        self._controller.turn_off_display()

    def mute_volume(self, mute):
        self._controller.mute_volume()

    def volume_up(self):
        self._controller.increase_volume()

    def volume_down(self):
        self._controller.decrease_volume()

    def select_source(self, source):
        self._controller.set_input(source)

    def update(self):
        self._controller.refresh()
