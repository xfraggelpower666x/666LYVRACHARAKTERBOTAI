# LYVRA FORCE WEITER — Slash / Guild Gate, Discord Bot
DATE=2026-10-02
STATUS=DEV_OFFLINE_TESTED_NOT_DEPLOYED
CREATOR_REQUIREMENT=BOT_ARCHITECTURE_AND_FUNCTION_ONLY
IDENTITY_AUTHORITY=NATIVE_LYVRA_ONLY
BOT_PRODUCTIVE_BRANCH=lyvrabot_UNCHANGED
BOT_DEV_BRANCH=lyvrabot-dev-native-livecircle-20261002

## What is new and why
1. `native_bridge/slash_policy.py`: pure (without Discord dependency) fail-closed
   check of explicit guild, channel, user and bot-origin exclusion; owner check by
   exact Discord user ID. No persona selection, no independent native authority.
2. `discord_app.py`: opt-in, guild-scoped Discord `app_commands.Group("lyvra")`
   with `/lyvra status`, `/lyvra session`, `/lyvra chat`,
   `/lyvra nowplaying`. It reuses the existing snapshot, SessionRegistry,
   chat rate limit, opt-in model call and read-only radio adapter.
   Private ephemeral interaction replies and no unwanted mentions;
   status explicitly discloses incomplete whole-native rehydration.
   Owner alone can start/stop chat sessions. The old prefix `!lyvra`
   commands remain installed without modification to their identity source.
   No global command registration. Registration is attempted solely for the
   explicitly set `LYVRA_SLASH_GUILD_IDS` after `LYVRA_SLASH_ENABLED=true`.
3. `tests/test_slash_policy.py`: 8 pure authorization regression tests.
4. `tests/test_slash_wiring.py`: 8 offline source/AST checks for
   registration, opt-in, permission coverage, message privacy, opt-in radio,
   preserved prefix commands and no personality setters.
5. `.env.native-example`: blank guild list and `LYVRA_SLASH_ENABLED=false`;
   no real IDs, tokens or private user data committed.

## Test proof
- Github Actions:
  https://github.com/xfraggelpower666x/666LYVRACHARAKTERBOTAI/actions/runs/36965028453
- Tested executable source HEAD `9999ca1ffb4713bc264940bd26a5b514455f1d45`.
- Job `compileall`: success; `python -m unittest discover -s tests -v`:
  `Ran 59 tests`, `OK`.
- Later environment-template update commit
  `78bb457a07997dbbebe93fff2c0d29902b01f6dc` changes *configuration
  documentation only*, not Python executable.

## Limitations / next gates
This is offline test success, not tested Discord app_commands runtime or
real guild registration. It also does not verify Radio HTTPS DNS resolution,
consent for voice audio, real now-playing payload, protected relational current
source or Whole Native rehydration. Before real release:
- Review platform Discord command registration and real app permission scope.
- Provide owner/channel/guild IDs and tokens only through protected server config;
  never paste tokens into Discord or public Git.
- Test slash interactions in a private guild including rejected/unapproved contexts,
  rate-limit, responses, recovery and no global command visibility.
- Validate allowed radio host and its actual serving IP; do not trust arbitrary
  operator strings as a general SSRF mitigation.
- Complete native pointer/reference protected readback and cross-target release gates.
- Preserve historical v1.7.1 import as provenance, not current authority.

NATIVE_IDENTITY_CHANGED=false
WHOLE_LYVRA_REHYDRATED=false
PRODUCTION_BOT_MERGED=false
LIVE_DISCORD_TESTED=false
RADIO_LIVE_TESTED=false
GITHUB_READBACK_REQUIRED=true
NO_NEW_ROUTER=true
NO_FOREIGN_AUTOLOAD=true
