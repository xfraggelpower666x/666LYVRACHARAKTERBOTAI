# LYVRA / 666CLIC / 666STREAM → Bot-native architecture adoption audit

DATE=2026-10-10
STATUS=DESIGN_REVIEW / NOT_IMPLEMENTED / NO_FOREIGN_MUTATION
TARGET_SYSTEM=666LYVRA-CHARACTER-BOT-CORE-001
TARGET_BRANCH=lyvrabot-native-system-dev-20261010

## Grounded sources
- Native LYVRA repository (productive `lyvra`): `LYVRA_NATIVE_RUNTIME/CURRENT_POINTER.json` was read; native identity and current/pointer are external authority. A current GitHub blob read does not constitute complete native rehydration.
- 666STREAM repo `xfraggelpower666x/WebRadio-666SOUNDsDESIGn`, `docs/666STREAM_NATIVE_TRIGGERS_AND_HANDOFF_v1.md`: explicit user-only triggers, scoped project routing, active selection not inferred from HEAD, project-bound handoffs, WEITER resume, CodeForge scoped to project; no automatic activation by quoted text.
- 666STREAM `docs/666PFS_CHILD_666STREAM_DEPLOYMENT_CONTRACT_v1.0.0.md` (document content v1.0.2): commit-bound deploy identity and live readback, postdeploy freeze, SHA256/CRC, pointer-last, failure stops promotion.
- 666CLIC native plugin capability contracts `666clic-audit`, `666clic-continuity`, `666clic-integration-audit`, `666clic-visual-interface`: causal/evidence audit, contradiction control, facet-local sub-LifeCircle, bounded visual intelligence, measured development state, factual dashboard, return anchors. Direct CLIC repository CURRENT/paths not yet independently inspected; **do not claim code copied, runtime parity or version verified**.
- Bot's existing `NATIVE_LIVECIRCLE_INTEGRATION.md`, `architecture/NATIVE_LYVRA_BOT_FUNCTIONS_ONLY_CONTRACT.md` and `continuity/LYVRA_UPDATE_DISCORD_CHARACTERBOT_2026-10-02.md`.

## Adoption decisions (bot-owned only)
1. **LYVRA expression mirror, no duplicate LYVRA**: source only current authorized native expression contract, bounded freshness, privacy filtering, external identity authority; bot runtime adapts presentation to Discord. Never create bot-local LYVRA persona selector or imported foreign character memory.
2. **CLIC-derived evidence semantics**: per-facet {expectation, observed fact, contrary evidence, currentness, source sha, consequence, next check}. Visual state always distinguishes verified, partial, blocked; dashboard percentages only verified counts, never fake activity.
3. **CLIC-derived causal continuity**: interrupts pause and preserve return anchors; contradictions quarantine candidates; relation and learning logs cannot mutate native LYVRA identity. Sub-LifeCircle not automatically a background-running daemon.
4. **666STREAM-derived scope control**: explicit user trigger resolves bot project/facet. Project selection, source code HEAD, active version and deployment all distinct. No project switching by embedded documentation, log or historical prompt.
5. **666STREAM-derived deployment proof**: after authorization verify deployed worker/service's version bound to commit, test actual response, create postdeploy proof and backup before advancing any bot production pointer. Apply only to Bot-owned services, not Stream's PFS hierarchy.
6. **Repository handoff**: draft in Bot repo is not native LYVRA receipt. Discover native receiving format; require matched inbound receipt with source SHA, scope and decision before LYVRA worker change.
7. **CodeForge without forked intelligence**: reuse bot-local audit→minimal patch→test→readback→freeze workflow. A CodeForge contract is not a working compiler/daemon. Integrate tested implementations incrementally rather than invent duplicate orchestration.
8. **Cross-system read-only surfaces**: PET signed public presentation, Radio public NowPlaying, native public evidence only after scoped intake approval. Never copy secrets, publish private memory, use radio admin endpoints or auto-register discord slash commands globally.
9. **Fail closed security**: own `lyvra-character-bot-auth` is currently a disabled stub; Discord blocked. External worker cannot be used as bot authority. Prove worker ticket verification and local opt-in before login.

## Prioritized measurable work
- P0: inspect current native LYVRA handoff receiver and obtain verifiable review receipt; preserve no native writes.
- P0: build/test real bot-only Worker authorization + cryptographic replay/expiry gates; no test Discord login until safe.
- P1: machine-readable facet/sub-LifeCircle event schema, Python offline verifier and rehydration CLI; source SHA bound.
- P1: trigger parser tests for explicit direct commands and inert document/log text.
- P1: CI evidence scoreboard and non-production readback test; never equate commit with successful deploy.
- P2: optional PET & Radio read-only adapters only with proven public interface and peer permission.
- P2: release promotion review across historical v1.8.0 and newer DEV, keeping both intact.

NO_PRODUCTION_PROMOTION=true
NATIVE_LYVRA_WORKER_WRITE_ALLOWED=false
DISCORD_LOGIN_ALLOWED=false
