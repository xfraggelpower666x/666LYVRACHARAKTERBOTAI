"""Bounded Discord *transport* policy, never a LYVRA identity or decision router.

Technical rules only: channel/guild isolation, anti-bot loops, rate limits,
response chunking. No character selection or autonomous content generation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from time import monotonic


def message_permitted(*, guild_id: int | None, channel_id: int,
                      author_is_bot: bool, allowed_channels: set[int],
                      mentioned: bool = False, mention_only: bool = False) -> bool:
    """Fail closed: no DMs/public channels or bots, optional explicit mention."""
    return (guild_id is not None and guild_id > 0
            and channel_id > 0 and channel_id in allowed_channels
            and not author_is_bot and (not mention_only or mentioned))


def split_discord_message(content: str, *, limit: int = 1800,
                          max_chunks: int = 6) -> list[str]:
    """Produce bounded Discord-safe chunks without silently truncating text."""
    if not isinstance(content, str):
        raise TypeError("Discord response must be text")
    if not 1 <= limit <= 2000 or max_chunks < 1:
        raise ValueError("Invalid Discord chunk limits")
    text = content.strip()
    if not text:
        return []
    if len(text) > limit * max_chunks:
        raise ValueError("Response exceeds configured per-message budget")
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        # Prefer a newline, then a space; guarantee progress for long tokens.
        cut = text.rfind("\n", 0, limit + 1)
        if cut < max(1, limit // 4):
            cut = text.rfind(" ", 0, limit + 1)
        if cut < max(1, limit // 4):
            cut = limit
        part = text[:cut].strip()
        if not part:  # Defensive safeguard for unusual whitespace.
            cut = limit
            part = text[:cut]
        chunks.append(part)
        text = text[cut:].lstrip()
        if len(chunks) > max_chunks:
            raise ValueError("Response requires too many Discord messages")
    return chunks


@dataclass
class InteractionThrottle:
    """Per-user, per-channel interval gate. State stays local and ephemeral."""
    cooldown_seconds: float = 3.0
    _seen: dict[tuple[int, int, int], float] = field(default_factory=dict)

    def allow(self, guild_id: int, channel_id: int, user_id: int,
              *, now: float | None = None) -> bool:
        if min(guild_id, channel_id, user_id) <= 0:
            return False
        timestamp = monotonic() if now is None else now
        key = (guild_id, channel_id, user_id)
        previous = self._seen.get(key)
        if previous is not None and timestamp >= previous and timestamp - previous < self.cooldown_seconds:
            return False
        if previous is not None and timestamp < previous:
            return False
        self._seen[key] = timestamp
        # Avoid unbounded growth without storing message contents.
        if len(self._seen) > 4096:
            threshold = timestamp - max(1.0, self.cooldown_seconds * 4)
            self._seen = {k: v for k, v in self._seen.items() if v >= threshold}
        return True

    def clear(self) -> None:
        self._seen.clear()
