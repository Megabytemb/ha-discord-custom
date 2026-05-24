"""Sensor platform for discord_custom."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .const import ACTIVITY_ICON_MAP, DOMAIN
from .coordinator import DiscordDataUpdateCoordinator
from .entity import DiscordEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            DiscordStatusSensor(coordinator=coordinator),
            DiscordActivitySensor(coordinator=coordinator),
            DiscordGamingSensor(coordinator=coordinator),
        ],
        True,
    )


class DiscordStatusSensor(DiscordEntity, SensorEntity):
    """discord_custom Sensor class."""

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = "Discord Status"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        if member := self.coordinator.data:
            return member.status.value
        return None

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        if member := self.coordinator.data:
            if display_avatar := member.display_avatar:
                return display_avatar.url
        return None

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if member := self.coordinator.data:
            return {
                "desktop_status": member.desktop_status.value,
                "mobile_status": member.mobile_status.value,
            }
        return {}

    @property
    def icon(self):
        """Return icon."""
        return "mdi:account"


class DiscordActivitySensor(DiscordEntity, SensorEntity):
    """discord_custom Sensor class."""

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = "Discord Activity"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        activity = self.coordinator.get_primary_activity(self.coordinator.data)
        return activity.name if activity else None

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if activity := self.coordinator.get_primary_activity(self.coordinator.data):
            data = activity.to_dict()
            if activity.type:
                data["type_str"] = activity.type.name
            return data
        return {}

    @property
    def icon(self):
        """Return icon."""
        if activity := self.coordinator.get_primary_activity(self.coordinator.data):
            return ACTIVITY_ICON_MAP.get(activity.type, "mdi:pencil")
        return "mdi:sleep"

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        if activity := self.coordinator.get_primary_activity(self.coordinator.data):
            return self.coordinator.async_get_icon_for_activity(activity)
        return None


class DiscordGamingSensor(DiscordEntity, SensorEntity):
    """Sensor for whether the tracked user is gaming."""

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = "Discord Gaming"

    @property
    def native_value(self) -> str | None:
        """Return the current game name or not gaming."""
        if activity := self.coordinator.get_game_activity(self.coordinator.data):
            return activity.name
        return "Not gaming"

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if activity := self.coordinator.get_game_activity(self.coordinator.data):
            return {
                "gaming": True,
                "game": activity.name,
                "type": activity.type.name if activity.type else None,
                "details": activity.to_dict(),
            }
        return {"gaming": False}

    @property
    def icon(self):
        """Return icon."""
        if self.coordinator.get_game_activity(self.coordinator.data):
            return "mdi:controller"
        return "mdi:sleep"

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        if activity := self.coordinator.get_game_activity(self.coordinator.data):
            return self.coordinator.async_get_icon_for_activity(activity)
        return None
