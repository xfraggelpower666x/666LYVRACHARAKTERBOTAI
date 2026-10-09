# LYVRA Character Bot — CURRENT MERGED DEVELOPMENT CANDIDATE (2026-10-10)

STATUS: **MERGED_DEV_CANDIDATE / DISCORD_OFFLINE / NOT_RELEASED**.

This branch is the **latest combined development candidate**, not a new verified product release or native LYVRA authority. It is deliberately separate from default `lyvrabot` and the original `lyvrabot-dev-native-livecircle-20261002`.

## Provenance

- Main source: `lyvrabot` HEAD `9fcfe324f4b56cef359a5337bae1d6a24fb71fc6` (including the historical Drive link document).
- DEV source: `lyvrabot-dev-native-livecircle-20261002` HEAD `be37a3af264ea30e2d40c5486b7142dda4bd6ef4`.
- Branched from DEV; cherry-picked by exact source contents (not Git ancestry) the three mainline native-change TODO watcher files, plus historical Drive archive navigation.
- Existing DEV Discord adapter/native_bridge/LiveCircle/radio-readonly/tests remain preserved.
- Discord login startup was **explicitly blocked** in `discord_app.py` pending independently implementable worker authorization and full test. No authorization token or cryptographic verification is simulated.
- Historical v1.8.0 canonical and PC ZIPs were uploaded and matched byte-for-byte, but **not** overlaid onto current DEV code. See `history/DRIVE_ARCHIVES_AND_BRANCH_PROVENANCE_2026-10-10.md`.
- Existing `README.md` and `RELEASE_MANIFEST.json` remain at v1.7.1 to avoid inventing a v1.8+ production release.

## Release blockers

1. Pin/read back native LYVRA CURRENT_POINTER and current contracts, avoid identity promotion.
2. Integrate and verify independent local deployment intent and **cryptographically verified** worker authorization before any Discord login.
3. Run repository-wide offline test suite and regression checks (GitHub connector source readback is not CI).
4. Reconcile v1.8.0 ZIP modules selectively with the newer DEV architecture; run 3-way file conflict audit before any copy.
5. Verify family/Radio/Verba nonmutation, Discord guild permission scopes, safe E2E, and rollback.
6. Only then evaluate making this branch the default or issuing a new versioned release.

**Do not deploy, force-merge, rename old branch, delete historical branch or advertise production readiness.**
