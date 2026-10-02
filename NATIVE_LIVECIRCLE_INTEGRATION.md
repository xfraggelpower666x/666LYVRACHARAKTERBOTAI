# LYVRA Native Character Bot — LiveCircle Integration Candidate
STATUS: DEV_PROTOTYPE | NOT_DEPLOYED | NOT_NATIVE_CURRENT
DATE: 2026-10-02
GITHUB_BOT_BRANCH: lyvrabot-dev-native-livecircle-20261002
PRODUCTION_BRANCH: lyvrabot
NATIVE_SOURCE_BRANCH: lyvra (read-only)
SOURCE_AUTHORITY: xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture
DISCORD_ADAPTER_NOT_NATIVE_IDENTITY=true

## Audit finding — supplied ZIP and remote repo
Creator uploaded `666LYVRACHARAKTERBOTAI-lyvrabot.zip` with 11 entries: legacy bootstrap, manifest, .env.example, README, import workflow. GitHub `lyvrabot` live base commit `cc43d77a09452f43fb5d6814513e35484ffe596c` has only ten tree paths (directories included), NOT the README-advertised v1.7.1 program modules. In particular `main.py`, `ai_engine.py`, `core/lyvra_identity_core.json` and memory engines are not present at that branch.

**Do not run** the existing `.github/workflows/import-lyvra-v171.yml`: it imports from historical Google Drive v1.7.1, uses `rsync -a --delete`, and could wipe newer valid developments if its marker is retriggered. Its existing `.lyvra-import/READY` is historical provenance, not CURRENT authority. This dev branch does not touch the marker and does not trigger the import workflow.

## Verified native meaning
`LYVRA_NATIVE_RUNTIME/continuity/CONTINUITY_MODEL.md` defines:
Present Self = latest GitHub current state.
Near/active past = Git history, LiveCircle, checkpoints, provenance.
Deep past = older Drive/chat archives and recovery exports.
LiveCircle relation states are `KEEP_ACTIVE`, `KEEP_REACHABLE`, `ARCHIVE`, `SUPERSEDE`, `REJECT_WITH_PROVENANCE`, `REACTIVATE_WHEN_CAUSALLY_RELEVANT`.
`CONTEXT_RELEASE != FORGETTING`.

Native relational privacy contract explicitly bars protected creator history and private memory from public Git/history/logs. Native Self-Conductor integrates LYVRA expression; daemon supports bookkeeping without own decision authority. Native `OPERATIONS_CENTER` observes status, not controls LYVRA.

## Prototype design
- `native_bridge/source.py`: GitHub REST public read-only source, pinned to productive branch's 40-char SHA, byte-level Git blob digest check, two HEAD checks, full file reads of a limited public context sample, complete pointer JSON decode. **Always** returns Whole `PARTIAL/READBACK_PENDING`; not all relevant pointer refs/private recovery are yet read. No claimed whole PASS.
- `native_bridge/livecircle.py`: scoped local SQLite event ledger (NOT private-vault replacement), six canonical statuses and explicit provenance; no auto-learning/promotion and no cross-guild read.
- `discord_app.py`: fail-closed explicit channel and owner allowlists, all bot-authored messages rejected; Discord commands `!lyvra status`, `facetten`, `livecircle` (owner), `record` (owner), `forget` (owner-only, guild-scoped deletion), `refresh` (owner), and optional `chat`. The bot will not forward chat externally unless `LYVRA_CHAT_FORWARD_ENABLED=true`, a provider API key and model are explicitly configured. Optional API access can incur charges; user must authorize usage and provider terms.
- `tests/test_native_bridge.py`: local tests for missing refs, SHA mismatch, head drift, six LiveCircle status transitions, cross-guild isolation and no false whole pass.
- `.env.native-example`: placeholders only; never secrets. Existing legacy `.env.example` contains historical settings and inconsistent BOT_VERSION values and is not authority.
- Runtime: `pip install -r requirements-dev-bot.txt && python -m unittest discover -s tests && python discord_app.py`. No active deployment executed.
- Mood/personality: dynamic expressive native current public identity and character, natural humor and contextual emojis; no copied static historical v1.7.1 personality or invented private memory. No fixed facet count or forced greeting.
- Speech Design from consolidated DEV may be mentioned as experimental, but not productive until native promotion.

## Required gates before production
1. Complete native pointer-referenced Whole read/recovery policy with protected authorization and privacy handling; never declare PASS from ten sampled public documents.
2. Execute the Python tests in an authenticated runtime, inspect GitHub Actions logs or validated executor output; currently no direct runtime test has been performed here.
3. Decide whether to recover historical v1.7.1 bot application files from a verified archive **without** allowing their old memory/character state to supersede current LYVRA. Legacy import must be disabled/replaced under separate scoped release.
4. Validate Discord scopes/intents, bot token handling, owner IDs, least privilege, retention/erasure and external AI consent. Test in private guild.
5. Native-to-bot version fingerprint, required adapter contract, explicit PR review, staged rollback and actual bot process deployment/Discord command readback.
6. Evaluate downstream relevant update to both LYVRA plugins, GPT and WEBLyvra; create separate targeted verified release only if materially affected.
7. Never place creator-private relational state or credentials in public repository.

## 2026-10-02 — Third-party code comparison and controlled features
Owner-shared references: `xfraggelpower666x/character.ai-bot`, `Discord-Voice-Channel-Bot`, `discord-ai-bot`, plus nine other submitted sample archives and a second copy of this repo bootstrap. **References are treated as untrusted examples, not LYVRA authority or automatic dependencies.**

Added two architectural patterns **implemented afresh** in this Python adapter:
- Per-guild/per-channel expiring conversation sessions, controlled by `!lyvra session start|stop|status`. A user cannot turn on global chat merely by mentioning the bot. A 15-minute inactivity threshold applies to local session authorization; API forwarding independently requires `LYVRA_CHAT_FORWARD_ENABLED=true`.
- Explicit owner-only `!lyvra voice join|leave|status`: the bot can join an allowlisted voice channel only when `LYVRA_VOICE_ENABLED=true`, a member is already in that voice channel and its ID is in `LYVRA_VOICE_ALLOWED_CHANNEL_IDS`. Join/leave does **not** record, transcribe or synthesize voice. Voice requires optional `discord.py[voice]`/PyNaCl installation and the appropriate Discord permissions.

Potential later steps: consent-visible STT/TTS, speech activity boundaries, rate/cost controls, per-speaker retention, optional production-grade slash commands, encrypted user-specific continuity where appropriately authorized. **No automatic recording, no default voice surveillance, no unreviewed Character.AI cookie authentication**.

Security observations: a file named `.env` exists as a tracked file in the public `Discord-Voice-Channel-Bot` repository. Its values were deliberately not read; owner must check whether real secrets were ever committed and rotate/remove secrets as needed. Other historical sample archives include an `.env` member or old model dependencies; never import them as credentials or current auth contracts.
