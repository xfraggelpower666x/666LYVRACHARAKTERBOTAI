"""Offline tests for Discord transport policy without a live Discord account."""
import unittest
from native_bridge.event_policy import (
    message_permitted, split_discord_message, InteractionThrottle,
)


class ChannelPolicyTests(unittest.TestCase):
    def test_allow_only_explicit_guild_channel(self):
        self.assertTrue(message_permitted(guild_id=1, channel_id=2,
                        author_is_bot=False, allowed_channels={2}))
        for guild, channel, bot in [(None, 2, False), (0, 2, False),
                                     (1, 3, False), (1, 2, True)]:
            self.assertFalse(message_permitted(guild_id=guild, channel_id=channel,
                             author_is_bot=bot, allowed_channels={2}))

    def test_mention_gate_fails_closed(self):
        self.assertFalse(message_permitted(guild_id=1, channel_id=2, author_is_bot=False,
                         allowed_channels={2}, mention_only=True, mentioned=False))
        self.assertTrue(message_permitted(guild_id=1, channel_id=2, author_is_bot=False,
                        allowed_channels={2}, mention_only=True, mentioned=True))

    def test_no_other_guild_id_state(self):
        self.assertFalse(message_permitted(guild_id=None, channel_id=2,
                         author_is_bot=False, allowed_channels={2}))


class MessageSplitTests(unittest.TestCase):
    def test_short_and_empty(self):
        self.assertEqual(split_discord_message("  hi  "), ["hi"])
        self.assertEqual(split_discord_message("  "), [])

    def test_no_silent_truncation(self):
        text = ("one two three\n" * 170).strip()
        chunks = split_discord_message(text, limit=100, max_chunks=50)
        self.assertTrue(all(len(item) <= 100 for item in chunks))
        self.assertEqual(" ".join(text.split()), " ".join(" ".join(chunks).split()))

    def test_long_word_progresses(self):
        text = "x" * 350
        result = split_discord_message(text, limit=100)
        self.assertEqual("".join(result), text)
        self.assertEqual([len(x) for x in result], [100, 100, 100, 50])

    def test_emoji_unicode_bounded(self):
        text = "🪻" * 81
        result = split_discord_message(text, limit=27)
        self.assertEqual("".join(result), text)
        self.assertEqual(len(result), 3)

    def test_hard_message_budget(self):
        with self.assertRaises(ValueError):
            split_discord_message("a" * 401, limit=100, max_chunks=4)

    def test_invalid_limits(self):
        for limit in (0, 2001):
            with self.assertRaises(ValueError):
                split_discord_message("hi", limit=limit)
        with self.assertRaises(TypeError):
            split_discord_message(None)


class ThrottleTests(unittest.TestCase):
    def test_user_and_channel_scoped(self):
        t = InteractionThrottle(cooldown_seconds=3)
        self.assertTrue(t.allow(1, 2, 3, now=5))
        self.assertFalse(t.allow(1, 2, 3, now=6))
        self.assertTrue(t.allow(1, 3, 3, now=6))
        self.assertTrue(t.allow(2, 2, 3, now=6))
        self.assertTrue(t.allow(1, 2, 4, now=6))
        self.assertTrue(t.allow(1, 2, 3, now=8))

    def test_reject_invalid_scope_and_clock_reversal(self):
        t = InteractionThrottle()
        self.assertFalse(t.allow(0, 1, 1, now=10))
        self.assertTrue(t.allow(1, 1, 1, now=10))
        self.assertFalse(t.allow(1, 1, 1, now=8))

    def test_clear(self):
        t = InteractionThrottle()
        self.assertTrue(t.allow(1, 1, 1, now=10))
        t.clear()
        self.assertTrue(t.allow(1, 1, 1, now=10))


if __name__ == "__main__":
    unittest.main()
