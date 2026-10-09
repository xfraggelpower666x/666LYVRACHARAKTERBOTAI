# Deterministic rehydration contract

1. Identify the exact bot repository and currently selected branch; verify remote HEAD and branch divergence without choosing a new production head.
2. Read IDENTITY.md, MANIFEST.json, CURRENT_POINTER.json, this protocol and relevant facet records at pinned ref.
3. Read original main `lyvrabot`, original DEV `lyvrabot-dev-native-livecircle-20261002`, merged source branch and current system DEV branch. Preserve their full histories.
4. Read historical Drive link evidence and verify original v1.8.0 ZIP hashes when bytes are available; archives are history, not active runtime.
5. Inspect code under `discord_app.py`, `native_bridge/`, `automation/`; verify current Discord offline gate. Never call bot.run or start Discord during rehydration.
6. Check each sub-LifeCircle's unresolved work and any human-reviewed receipts. Compute `PASS` only for tested checks; use `PARTIAL`, `READBACK_PENDING` or `CONFLICT` otherwise.
7. External native LYVRA: consume ONLY public, scoped read-only evidence when permitted. Any LYVRA-worker change needs verified repo-native inbound handoff and approval. No invented receipt.
8. Resume development only from last evidence-backed checkpoint; if a writer lock or conflicting SHA is detected, halt mutation and rebase after recheck.

The Bot CURRENT_POINTER is a local navigation document, not a global LYVRA pointer, authority promotion, or a proof of deploy readiness.
