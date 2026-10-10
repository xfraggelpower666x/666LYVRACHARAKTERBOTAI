# LYVRA Character Bot — Creator Source Cross-Audit
DATE=2026-10-02
STATUS=DEV_EVIDENCE_NOT_AUTOMATIC_IMPORT
OWNER_APPROVAL_SCOPE=EVALUATE_REFERENCES_AND_ADDITIVE_SAFE_DEV_IMPLEMENTATION
BOT_ROOT_AUTHORITY=NONE
LYVRA_NATIVE_SOURCE=GITHUB_PRODUCTIVE_lyvra
PROPRIETARY_PROVIDER_AUTHENTICATION_IMPORT=FORBIDDEN

## Source mapping: owner-provided GitHub URLs, read via connected GitHub
1. `xfraggelpower666x/character.ai-bot`, branch `main`, tree SHA `d078d9a92f68a7d6fbec4c23bd100125030dacf8`: small Node/Discord bot with per-character interactions; a global single `activeChat` session, unofficial `node_characterai` and manual browser-derived Character.AI token documented in README. Project itself warns recent Character.AI changes impair connectivity. **Not** a stable source for LYVRA identity, auth or production chat. Portable *idea*: explicit start/stop conversation. Implemented independently as guild+channel local sessions with timeout; no vendor cookie import.
2. `xfraggelpower666x/Discord-Voice-Channel-Bot`, branch `main`, tree SHA `43892e73a3d468d98d0feb55a4250b3b55e83aa5`: Node Voice transport using slash `/join`, `/leave`, Whisper transcription and Azure TTS example; global `memoryManager.js` and editable `personality.json` are **not** LYVRA native authority. Its public Git tree **contains a tracked `.env` file**, contents purposely NOT inspected. Require owner to review history, remove/rotate any real credentials if present. Inspired a separate default-OFF voice **join/leave/status** with owner/channel allowlists, **without STT/TTS/audio capture**.
3. `xfraggelpower666x/discord-ai-bot`, branch `main`, tree SHA `1f26ceca7a36b69d41eda8b6fb191922f730e7b4`: Go administration/chat/image and role-check patterns, plus restart/game server functions. Role names alone are not stable permissions. Use explicit owner IDs and allowlisted channels in current Python adapter, avoid separate Go admin daemon, side-effectful bot restarts or autonomous moderation until scoped review. Its emoji update handler assumes last element exists, a potential empty-list fragility; not cloned.
These repos are references; no deployed source lineage or automatic merge is inferred.

## ZIP inventory: statically examined, archives were NOT executed
User attachments checked for path traversal and aggregate inventory; all 10 ZIPs show zero absolute/parent-traversal member names in the initial manifest scan. That does NOT imply malware-free content or dependency safety.
- `character.ai-bot-main.zip` (7 files): mirrors the Node unofficial Character.AI session concept; same concern as owner GitHub.
- `CharacterAI-Discord-Bot-master.zip` (52 files): C# binary `CharacterAI.dll` and EF migrations, project declares itself unsupported/absorbed elsewhere. No binary loading or reuse; possible UI idea of parallel chats only.
- `ChatGPT-Discord-BOT-main.zip` (34 files): historical Node chat / Firebase state with CodeQL/OSSAR/dependency workflows; review *principles* of CI and session separation, not Firebase remote memory or old dependencies.
- `OpenAI-Discord-Bot-main.zip` (26 files): historical Node/SQLite and slash `ask/chat/image` patterns; contains a `.env` entry whose checked values were empty in this archive. Do not import any env file, store or old model interface.
- `openai-discord-main.zip` (28 files): historical TypeScript Docker/chat embedding; avoid duplicate Node runtime, model APIs and implicit costs.
- `midjourney-bot-master.zip` (15 files): Replicate/visual image commands and provider billing changes; no assumed free provider access; optional creative/media scope only after separate request.
- `RoK-discord-bots-main.zip` (31 files): game/server automation and heavyweight model binaries; unrelated to LYVRA character continuity.
- `666-sounds-psytrance-engine-master.zip` (4377 files, many `node_modules`): music design/lyrics/psychoacoustic references may later inform native **music analytics** through explicit evidence and creator consent, not independent bot engine or new music controller. Ignore bundled node_modules as source authority.
- `666-sounds-psytrance-engine-audit-lint-security-pwa-fixes.zip` (16 files): code quality/PWA hints in separate web/music context; not a Discord runtime dependency.
- `666LYVRACHARAKTERBOTAI-lyvrabot(1).zip` (7 files): duplicate historical import bootstrap; do not replay old v1.7.1 Google Drive import or `rsync --delete`.

## License and rights
No source code from external projects was copied into the LYVRA bot in this audit. The separate reference repos contain different license declarations (Voice sample MIT, Go admin BSD-3-Clause, Character.ai package metadata ISC). Third-party libraries and provider SDKs require current license/dependency/security checks prior to adoption. Uploaded packages do not authorize publication of third-party assets or private API material.

## Implemented in owned bot **DEV branch**, independently authored
- `native_bridge/interaction.py`: 15-minute in-memory guild+channel Chat Session with no persistent chat transcript, and pure voice eligibility guard.
- `discord_app.py`: owner-only `!lyvra session start|stop|status`, owner-only `!lyvra voice join|leave|status`. Active channel sessions gate `chat` even when external API is otherwise opted in.
- `.env.native-example`: `LYVRA_VOICE_ENABLED=false` and allowlisted voice channel IDs.
- `requirements-optional-voice.txt`: optional Discord Voice transport package. No audio reception/recording/transcription/synthesis.
- `tests/test_native_bridge.py`: session expiry, scope isolation, voice default-deny and permissions.
- Existing LiveCircle SQLite and pinned read-only native source remain the only prototype continuity/identity inputs, always PARTIAL.

## Risk and next phase
1. Mandatory Discord server/channel/voice consent rules, audit real bot roles/intents and check exposed `.env` files for secrets **without** printing them to public logs.
2. Complete source Native full-pointer references and protected-relational privacy gates before claiming Whole rehydrated. Public source-only character projection remains partial.
3. Consider real-time voice transcription + response synthesis only via separately authorized and recorded consent, provider budget and retention rules; no listening by merely joining.
4. If adding image functions, separate image generation provider terms, content/privacy, quotas, moderation and cost controls.
5. Avoid importing legacy compiled DLL, Go background admin, Firebase state or outdated Character.AI user cookies.
6. Use native cross-target release propagation: both private Plugins, GPT, WEBLYVRA, Discord bot. An applicable change must get a target-specific readback, not just an audit checklist.
