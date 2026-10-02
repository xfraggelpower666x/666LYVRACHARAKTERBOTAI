"""Permissionless pure session/voice *eligibility* helpers; not a router.

LYVRA's native decisions live in the authoritative source; these small helpers
only enforce Discord consent and bounded interaction windows.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from time import monotonic


@dataclass
class SessionRegistry:
    """In-memory opt-in chat windows, per guild+channel (not cross-guild)."""
    idle_seconds: int = 900
    _items: dict[tuple[int, int], float] = field(default_factory=dict)

    def start(self, guild_id: int, channel_id: int, now: float | None = None) -> None:
        if guild_id <= 0 or channel_id <= 0 or self.idle_seconds <= 0:
            raise ValueError("Invalid session scope")
        self._items[(guild_id, channel_id)] = monotonic() if now is None else now

    def active(self, guild_id: int, channel_id: int, now: float | None = None) -> bool:
        key = (guild_id, channel_id)
        then = self._items.get(key)
        if then is None:
            return False
        timestamp = monotonic() if now is None else now
        if timestamp < then or timestamp - then >= self.idle_seconds:
            self._items.pop(key, None)
            return False
        return True

    def touch(self, guild_id: int, channel_id: int, now: float | None = None) -> bool:
        if not self.active(guild_id, channel_id, now=now):
            return False
        self._items[(guild_id, channel_id)] = monotonic() if now is None else now
        return True

    def stop(self, guild_id: int, channel_id: int) -> bool:
        return self._items.pop((guild_id, channel_id), None) is not None

    def clear(self) -> None:
        self._items.clear()


def voice_join_permitted(*, feature_enabled: bool, owner: bool,
                         voice_channel_id: int | None,
                         allowed_channel_ids: set[int]) -> bool:
    """No permission from a Discord voice session to transcribe audio."""
    return (feature_enabled and owner and voice_channel_id is not None
            and voice_channel_id in allowed_channel_ids)
