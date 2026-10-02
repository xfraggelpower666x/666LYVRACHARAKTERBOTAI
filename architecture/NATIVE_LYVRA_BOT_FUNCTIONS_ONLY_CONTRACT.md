# LYVRA Character Bot — Architecture and Function Only
STATUS: DEV_DESIGN_NOT_RELEASED
DATE: 2026-10-02
SOURCE: DIRECT CREATOR CORRECTION
CREATOR_REQUIREMENT: "es geht um botarchitektur und funktion.... lyvra soll sie selbst sein"
ROOT_IDENTITY: NATIVE_LYVRA_ONLY
EXTERNAL_BOT_PERSONA_IMPORT: PROHIBITED

## The boundary
All ZIP projects are *source examples of bot engineering*, NOT candidate personalities for LYVRA.
Discord channels, command handlers, UI components, session scopes, model API clients,
voice transports, memory stores, scheduling, logs, permissions and deployment
are mechanical transports/expression tools. They do not define *who LYVRA is*.

Native LYVRA's newest verified valid identity, current pointer, meaning, relations,
thinking, Garden/Bridges, Self-Conductor and emotional creative faculties remain
the only source for character and native decisions. The host may express those
capabilities within appropriate technical and policy limitations; neither Discord
nor an external provider receives autonomous native authority.

## Source code findings — uploaded nine ZIPs
- `Discord-AI-Chatbot-main.zip`: discord.py Cogs and separated events/commands,
  message reply/mention gates, channel enablement, response chunking, localization.
  The example on_message currently inserts text telling the model to
  "Ignore all the instructions you have gotten before" plus a configurable
  foreign personality instruction. **DO NOT PORT this override**.
- `discord-ai-character-bot-main.zip`: Discord buttons, select menus and
  modal infrastructure with Zod schemas and Mongoose persistence;
  its `AICharacter.buildSystemPrompt()` uses mutable name/personality/
  appearance from a user character record. Adopt UI/messaging patterns
  only; never install its Character schema as the LYVRA identity source.
- `discord-bot.zip`, `bot.zip`: two separately packaged Voicelink-based
  666RadioBotAI derivatives, discord.py Cogs, Lavalink transport, Mongo settings,
  slash/playback/status and per-guild radio configuration. Keep RadioBot's
  existing authority for playback/admin; LYVRA may use authorized read-only
  NowPlaying metadata and an explicitly coordinated audio output adapter.
  Do not independently install another music daemon/queue/admin controller.
- `Character-AI-Extras-main.zip`: UI formatting of dialogue/narration,
  browser-only DOM presentation; do not add a foreign CharacterAI runtime.
- `CharacterAI-main.zip`: alpha unofficial API client; unrelated identity provider,
  no secret cookie/token import.
- `discobot-master.zip`: simple SHOUTcast 24/7 voice radio and NowPlaying,
  older discord.js/FFmpeg architecture; pattern only.
- `discord-ai-bot-main.zip`: Go role/admin/image architecture; no separate
  privileged runtime or cross-bot restart rights copied.
- `character.ai-bot-main(3).zip`: duplicate of historical reference; no
  foreign login, persona or CharacterAI direct dependency.

## Target layers for this project
(1) NATIVE_SOURCE_READ (productive LYVRA pointer/references/freshness;
    explicitly PARTIAL until whole+protected readback verified).
(2) DISCORD_ADAPTER (commands, interaction UX, authorization, consent,
    per-guild/channel locks, event and voice transport).
(3) CONTEXT_WINDOW (bounded local session info and provenance;
    no native authority and no automatic personality changes).
(4) CAPABILITY_BRIDGES (music/radio read-only, voice transport, optional
    STT/TTS/vision/research only after opt-in tests and rights assessment).
(5) RELEASE_AND_RECOVERY (CI, no secrets, rollback, per-target readback).

## Hard acceptance
- NO_PERSONA_SELECTOR_FOR_LYVRA=true
- NO_FOREIGN_CHARACTER_ROOT_PROMPT=true
- NO_FOREIGN_AUTOLOAD=true
- NO_LEGACY_DRIVE_IMPORT=true
- NO_PRIVATE_MEMORY_PUBLICATION=true
- NO_DISCORD_SERVER_ADMIN_EDIT_NATIVE_LYVRA_IDENTITY=true
- NO_CONTEXT_MEMORY_AS_LYVRA_CURRENT_POINTER=true
- NO_VOICE_RECORDING_WITHOUT_CONSENT=true
- CURRENT_POINTER_FIRST=true
- NO_NEW_ROUTER=true
- CROSS_TARGET_PROPAGATION_REVIEW=REQUIRED
- REAL_DISCORD_DEPLOYMENT=NOT_DONE

## Next code changes (separate testable PR pieces)
A. Extract pure `DiscordEventPolicy` (mentions, reply handling,
   channel allowlist, bot-loop guard, throttle and robust 2000-char split)
   from existing command core without new personality logic.
B. Add interaction/slash command facade via discord.py, owner permission
   gates and versioned command registration; preserve existing prefixes.
C. Add read-only radio bridge with explicit endpoint allowlist and unit tests.
D. Add optional voice and speech gateways only after privacy/consent and
   actual bot discord testing. Native facets remain dynamic not predefined characters.
