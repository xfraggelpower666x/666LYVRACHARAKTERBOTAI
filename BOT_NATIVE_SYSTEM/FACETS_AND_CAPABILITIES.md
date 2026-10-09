# Facets and capabilities

Every facet has its own read-only or bot-repository-local scope, sub-LifeCircle, validation, recovery and evidence state. No facet gains native LYVRA authority through naming.

| Facet | Responsibility | Capability | Release gate |
|---|---|---|---|
| Identity Boundary | preserve LYVRA's native identity | check adapter contracts, public provenance | never overwrite identity |
| Repository Continuity | inspect history and parallel branches | pinned commits and non-destructive diffs | conflict review |
| LiveCircle | causal bot engineering event log | add/supersede/restore local records | never native memory |
| Rehydration | resolve current bot repository state | read pointer, manifest, HEAD, receipts, blockers | fail on conflict |
| CodeForge | engineering orchestration | audit→plan→patch→test→readback→recovery | protected writes |
| Trigger Router | textual command dispatch | exact bot-prefix commands, audit-only fallback | no implicit side effects |
| Security Worker | own cloudflare auth worker | dedicated contract, offline hardlock | independent ticket proof |
| Discord Transport | commands, privacy, permissions | offline-first guild-scoped adapter | no login by default |
| Native Bridge | public LYVRA evidence consumer | read-only SHA anchored contracts | no Whole-PASS inference |
| Radio Readonly | NowPlaying metadata | allowlisted GET only | no admin/skip |
| PET Readonly | signed, public PET expression | validate signature, freshness and scope | LYVRA handoff receipt |
| Release & Recovery | protect two original branches and drive archives | backups, rollback proofs, change receipts | separate release decision |

Modules and capabilities already implemented in `discord_app.py` and `native_bridge/` remain the code authority for their actual behavior; this registry does not magically implement missing functions.
