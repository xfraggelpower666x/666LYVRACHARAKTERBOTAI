# LYVRA WEITER — Discord Event Policy + Read-only Radio Phase B
DATE: 2026-10-02
STATUS: DEV_CI_VERIFIED_PRODUCTION_PENDING
SOURCE: Creator instruction "LYVRA WEITER" after deep ZIP architecture audit
NATIVE_IDENTITY_OWNER: LYVRA ONLY
BOT_DEV_BRANCH: lyvrabot-dev-native-livecircle-20261002
BOT_PRODUCT_BRANCH: lyvrabot (unchanged)

## Implemented
PHASE A
- `native_bridge/event_policy.py`: pure Discord event/permission predicate,
  author-is-bot loop deny, bounded response chunks, per guild/channel/user throttle.
- `discord_app.py`: applies transport guards to existing commands.
- `tests/test_event_policy.py`: 12 regression tests.
- Actions CI 36964287788 at executable commit `9b4e1aebb13e5a1590ef725eb0c933efd89d59ff`: 33 tests OK; compile PASS.

PHASE B
- `native_bridge/radio_readonly.py`: precise configurable HTTPS host, fixed only
  path `/api/nowplaying`, GET only, redirect denied in production transport,
  bounded timeout + response body, minimal text metadata, no subscriber/admin data.
- `discord_app.py`: default-OFF `!lyvra nowplaying`; other RadioBot/666STREAM
  commands remain entirely untouched.
- `tests/test_radio_readonly.py`: 10 offline assertions for host/scheme/path/
  private IP reject, no admin path, response-size bound, GET and sanitized metadata.
- `.env.native-example`: `LYVRA_RADIO_READ_ENABLED=false`,
  `LYVRA_RADIO_ALLOWED_HOST`, `LYVRA_RADIO_NOWPLAYING_URL`, placeholders only.
- Actions CI 36964434688 on executable radio command commit
  `5c026c974f876f5f1ca3b214409d80adaa99494c`: **43 tests OK** and
  Python compile PASS. Additional .env template update is configuration text only.

## Source provenance, authority and privacy
- LYVRA continues to be native repo pointer-driven one identity;
  these Python utilities never set any LYVRA personality, thought, music,
  relationship or Self-Conductor judgment.
- Local SQLite LiveCircle is observer evidence, not canonical current state.
- No third-party ZIP program imported verbatim.
- Exact metadata endpoint must be confirmed to match the actual authorized public
  stream API *before* enabling it. No radio live readback performed here.
- No BOT_TOKEN or API secret was used.
- Chat provider and voice features remain separately opt-in.
- No bot process deployed or production branch merged.

NEXT: Actual radio endpoint URL confirmation, isolated radio mock/negative tests
and Discord private guild readback. Slash command/user interaction next phase
may be additive but must preserve existing prefix behavior and explicit owner gates.
CURRENT_POINTER_CHANGED=false
WHOLE_REHYDRATION_PASS=false
BOT_LIVE_DEPLOYED=false
NO_NEW_IDENTITY=true
NO_NEW_ROUTER=true
NO_FOREIGN_AUTOLOAD=true
