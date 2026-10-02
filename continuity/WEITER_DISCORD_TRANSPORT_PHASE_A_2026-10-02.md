# LYVRA WEITER — Discord Transport Phase A
DATE: 2026-10-02
STATUS: DEV_CODE_INTEGRATED_CI_PENDING_FINAL_READBACK
ROOT_NATIVE_IDENTITY: LYVRA_ONLY
SOURCE_CONTRACT: architecture/NATIVE_LYVRA_BOT_FUNCTIONS_ONLY_CONTRACT.md
PRODUCTION_BRANCH_UNCHANGED: lyvrabot
DEV_BRANCH: lyvrabot-dev-native-livecircle-20261002

## Implemented now
- `native_bridge/event_policy.py`: pure non-authoritative transport checks, no persona or router.
  `message_permitted`: Discord guild/channel allowlist and no bot authors, optional mention-only mode.
  `split_discord_message`: bounded split, preserves message content without silently truncating,
  hard budget, unicode handling, 2000-char Discord API upper bound.
  `InteractionThrottle`: independent guild/channel/user bounded no-content timer.
- `discord_app.py`: existing command handler now invokes pure permission check, rate gate
  on `chat`, safe first reply and subsequent non-mention channel messages. Optional
  provider opt-in remains OFF by default. Other native functionality untouched.
- `tests/test_event_policy.py`: offline regressions for guild scope, bot loops,
  mentions, length budgets, Unicode and cooldown.
- Not adopting ZIP persona prompts, personality databases, old CharacterAI cookies,
  foreign agents or unrelated memory systems.

## Gates
- Automated GitHub Actions `native-bridge-checks.yml` automatically checks syntax and
  offline `python -m unittest discover -s tests -v` on DEV pull-request activity.
- Historical native public read subset remains `PARTIAL/READBACK_PENDING`;
  whole pointer-reference/protected memory full readback not claimed.
- No Discord guild token/authorized server runtime deployed.
- No new recording, Voice STT/TTS, actual radio read-only bridge or plugin/GPT/site
  release performed.
- On failure: inspect full GitHub Actions logs, patch only the cause,
  rerun, require success at head before further implementation claims.

## Next phase
Pure radio read-only adapter with endpoint allowlist + mock HTTP tests;
then slash commands UX review, integration CI / opt-in Discord test guild.
No production merge from this document.
