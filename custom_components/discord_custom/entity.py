"""DiscordEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import ATTRIBUTION, DOMAIN, INTEGRATION_VERSION, NAME
from .coordinator import DiscordDataUpdateCoordinator


class DiscordEntity(CoordinatorEntity):
    """DiscordEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.user_id)},
            name=NAME,
            model=INTEGRATION_VERSION,
            manufacturer=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        unique_id = (
            self.coordinator.config_entry.entry_id + "-" + slugify(self._attr_name)
        )
        return unique_id
