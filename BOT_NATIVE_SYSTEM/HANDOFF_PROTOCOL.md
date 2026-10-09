# Bot ↔ native LYVRA repository handoff

Types: PROPOSAL, RECEIPT, DECISION, RETURN_HANDOFF.
Required fields: ID, source repository/branch/head, destination repository/branch, scope, affected worker, precise read-only vs change request, evidence paths, requested decision, privacy classification, expiry, and non-authority flag.

Possible states: DRAFT, OUTBOUND_SAVED, TRANSPORT_UNVERIFIED, NATIVE_RECEIVED, REJECTED, APPROVED_SCOPE_ONLY, COMPLETED_WITH_READBACK.

Never equate saving outbound file in bot repo with receipt in native repo. A real automated bridge must be demonstrated by a verified native inbox and receipt mechanism. No LYVRA-owned Worker may be changed on mere bot initiative; approval must be verified and target-specific.

Current coordination outbound: `handoffs/OUTBOUND_TO_LYVRA_CHARACTER_BOT_WORKER_COORDINATION_2026-10-10.md`; state OUTBOUND_SAVED / TRANSPORT_UNVERIFIED.
