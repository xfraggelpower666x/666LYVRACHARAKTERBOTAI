"""Offline slash interaction permissions — no Discord token or API requests."""
import unittest
from native_bridge.slash_policy import allowed_interaction, allowed_owner_interaction


class SlashPolicyTests(unittest.TestCase):
    def setUp(self):
        self.opts = dict(approved_guild_ids={10}, approved_channel_ids={20})

    def test_explicit_guild_and_channel(self):
        self.assertTrue(allowed_interaction(guild_id=10, channel_id=20,
                        user_id=30, user_is_bot=False, **self.opts))

    def test_reject_private_dms(self):
        self.assertFalse(allowed_interaction(guild_id=None, channel_id=20,
                         user_id=30, user_is_bot=False, **self.opts))

    def test_reject_other_server(self):
        self.assertFalse(allowed_interaction(guild_id=11, channel_id=20,
                         user_id=30, user_is_bot=False, **self.opts))

    def test_reject_other_channel(self):
        self.assertFalse(allowed_interaction(guild_id=10, channel_id=21,
                         user_id=30, user_is_bot=False, **self.opts))

    def test_reject_bot_authors(self):
        self.assertFalse(allowed_interaction(guild_id=10, channel_id=20,
                         user_id=30, user_is_bot=True, **self.opts))

    def test_reject_missing_user(self):
        self.assertFalse(allowed_interaction(guild_id=10, channel_id=20,
                         user_id=None, user_is_bot=False, **self.opts))

    def test_no_auto_allow_all(self):
        self.assertFalse(allowed_interaction(guild_id=10, channel_id=20,
                         user_id=30, user_is_bot=False,
                         approved_guild_ids=set(), approved_channel_ids={20}))

    def test_owner_requires_both_guards(self):
        self.assertFalse(allowed_owner_interaction(user_id=30, owner_ids={30},
                         interaction_allowed=False))
        self.assertFalse(allowed_owner_interaction(user_id=31, owner_ids={30},
                         interaction_allowed=True))
        self.assertTrue(allowed_owner_interaction(user_id=30, owner_ids={30},
                        interaction_allowed=True))


if __name__ == "__main__":
    unittest.main()
