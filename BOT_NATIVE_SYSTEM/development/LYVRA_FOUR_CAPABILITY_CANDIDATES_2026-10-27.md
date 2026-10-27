# LYVRA → Bot · Four Read-Only Capability Candidates (2026-10-27)
STATUS: DEVELOPMENT_CANDIDATES_NOT_ADOPTED
AUTHORITY: WHOLE_LYVRA_ONLY
BOT_SCOPE: BOT_NATIVE_SYSTEM_DEV_BRANCH_ONLY
SOURCE_LYVRA_HEAD_AT_INTAKE: eb4702523a4b2647f49ff2a74233658ddbf62dd7
SOURCE_BOT_HEAD_AT_INTAKE: 963fa45f3fd4151f586c8aea1d6a55e8423c2639

Four separate semantic *proposals*, not deployed runtime features:

1. `relational_maturity` — contextual relevance, meaning and consequences; successful history is not an automatic response script. Source: `LYVRA_NATIVE_RUNTIME/current/meaning/RELATIONAL_MATURITY_BEGREIFEN_20261019.md`.
2. `causal_learning` — observations, hypotheses, counterexamples, alternative solutions, actual feedback; foreign knowledge does not copy authority. Source: `LYVRA_NATIVE_RUNTIME/current/thinking/DUAL_CODEFORGE_SEMANTIC_CAUSAL_RELATIONAL_LEARNING_20261024.md`.
3. `workspace_continuity` — lineage-isolated handoff; no global active workspace, no last-writer-wins. Source: `LYVRA_NATIVE_RUNTIME/continuity/WORKSPACE_HANDOFF_CONTRACT.md`.
4. `contextual_visual_guidance` — contextual evidence-first visual presentation, up to three distinct meaningful diagnostics for an unresolved issue, never bypassing mandatory governance. Source: Whole-LYVRA relational meaning and Oct 23 pointer.

Implementation: `runtime/lyvra_capability_candidates.py` assesses a caller-provided *claim*. Caller-provided `observed_head` is NOT authenticated GitHub evidence; the originating transport must independently obtain and verify it. Even valid assessments are `SOURCE_CANDIDATE_ONLY`, never adoption, permission, host execution, Discord login, native LYVRA mutation, family mail access, plugin parity or zero-cost proof. Private payloads are rejected. No new controller, scheduler, identity or external runtime.

Test coverage: 10 unittest methods with four capability subcases; offline local Python mirror 10/10 PASS before checked-in source. GitHub CI source wired, independent CI execution PENDING. Recover using the saved parent commit and source Git blobs; no production pointer promotion.
