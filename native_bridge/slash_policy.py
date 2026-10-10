"""Pure least-privilege permission helpers for optional Discord slash commands.

No LYVRA identity, personality or native state decisions live here.
"""
from __future__ import annotations


def allowed_interaction(*, guild_id: int | None, channel_id: int | None,
                        user_id: int | None, user_is_bot: bool,
                        approved_guild_ids: set[int],
                        approved_channel_ids: set[int]) -> bool:
    """Require explicit guild AND channel authorization, never DMs or bot loops."""
    return (isinstance(guild_id, int) and guild_id > 0
            and isinstance(channel_id, int) and channel_id > 0
            and isinstance(user_id, int) and user_id > 0
            and guild_id in approved_guild_ids
            and channel_id in approved_channel_ids
            and not user_is_bot)


def allowed_owner_interaction(*, user_id: int | None, owner_ids: set[int],
                              interaction_allowed: bool) -> bool:
    """Owner permissions are exact Discord user IDs, never usernames or role claims."""
    return bool(interaction_allowed and user_id is not None and user_id in owner_ids)
