"""Offline contract tests for optional guild-only Discord slash facade.

No discord.py import, credentials, network or live bot are required.
Integration runtime is deliberately NOT asserted by these static checks.
"""
import ast
from pathlib import Path
import unittest


class SlashWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).resolve().parents[1] / "discord_app.py").read_text(
            encoding="utf-8")
        cls.tree = ast.parse(cls.source)
        cls.functions = {n.name: n for n in ast.walk(cls.tree)
                         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def test_guild_scoped_registration_only(self):
        self.assertIn("bot.tree.add_command(slash_group, guild=guild)", self.source)
        self.assertIn("bot.tree.sync(guild=guild)", self.source)
        self.assertNotIn("await bot.tree.sync()", self.source)

    def test_operator_opt_in_required(self):
        self.assertIn('on("LYVRA_SLASH_ENABLED")', self.source)
        self.assertIn('SLASH_GUILDS = ids("LYVRA_SLASH_GUILD_IDS")', self.source)

    def test_handlers_exist(self):
        for name in ("slash_status", "slash_session", "slash_chat", "slash_nowplaying"):
            self.assertIn(name, self.functions)
            self.assertIsInstance(self.functions[name], ast.AsyncFunctionDef)

    def test_slash_permissions_check(self):
        for name in ("slash_status", "slash_chat", "slash_nowplaying"):
            body = ast.unparse(self.functions[name])
            self.assertIn("interaction_allowed(interaction)", body)
        self.assertIn("interaction_owner(interaction)",
                      ast.unparse(self.functions["slash_session"]))

    def test_chat_consents_and_privacy(self):
        body = ast.unparse(self.functions["slash_chat"])
        self.assertIn("chat_sessions.active", body)
        self.assertIn("chat_throttle.allow", body)
        self.assertIn("ephemeral=True", body)
        self.assertIn("allowed_mentions=discord.AllowedMentions.none()", body)

    def test_radio_has_independent_optin(self):
        body = ast.unparse(self.functions["slash_nowplaying"])
        self.assertIn('LYVRA_RADIO_READ_ENABLED', body)
        self.assertIn("fetch_nowplaying", body)
        self.assertNotIn("skip", body)
        self.assertNotIn("preset", body)

    def test_prefix_bot_remains_registered(self):
        for prefix in ("cmd_status", "cmd_session", "cmd_chat",
                       "cmd_nowplaying", "cmd_voice"):
            self.assertIn(prefix, self.functions)

    def test_slash_cannot_manage_identity(self):
        for forbidden in ("set_personality", "set_identity", "set_canon",
                          "replace_identity", "set_family"):
            self.assertNotIn(f"def slash_{forbidden}", self.source)


if __name__ == "__main__":
    unittest.main()
