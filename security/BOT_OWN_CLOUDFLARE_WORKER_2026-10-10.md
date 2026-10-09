# Dedicated Cloudflare Worker — LYVRA Character Bot

Verified on 2026-10-10 (Europe/Berlin): Cloudflare account 666SOUNDsDESIGn has a new, bot-specific Worker **lyvra-character-bot-auth**.

## Separation
- Worker identity: `lyvra-character-bot-auth` (dedicated bot auth boundary).
- Unrelated native LYVRA Worker `lyvrasystem` and system-auth/pw Workers were not changed.
- This Worker is currently a **DISABLED / FAIL-CLOSED STUB**, not a functioning authorization issuer or verifier.
- GET `/health` reports `state=DISABLED`, `discord_deployment=false`, `worker_authorization=false`.
- All other requests return HTTP 403, `BOT_AUTH_NOT_CONFIGURED`, `discord_login_authorized=false`.
- Worker has **no secrets/bindings**; workers.dev subdomain is **disabled**.
- Cloudflare deployed version on initial readback: `86e8a032-1a88-47f2-b88c-8db7bd30e519` at 100%. This is NOT a production bot authorization release.

## Required implementation gates before activation
1. Define separate bot identity, audience, scoped challenge/response, nonce, expiry, replay protection, revocation, and exact verification contract.
2. Provision independent credentials safely in Cloudflare; do not copy/reuse `lyvrasystem` signing secrets.
3. Explicit local opt-in and valid remote verification **both required** prior to Discord login. Prevent fail-open on network errors.
4. Test invalid/missing/expired/replayed/wrong-audience tickets and network outage, with CI and a non-production endpoint.
5. Keep existing Radio/Detlef/Verba integrations untouched; isolate privileged actions.
6. Deploy a gated and tested implementation only after separate authorization.

## GitHub integration
Combined DEV candidate: `lyvrabot-merged-candidate-20261010`. Its `discord_app.py` explicitly denies Discord start until proper worker verification exists. Neither this document nor this worker modifies the native LYVRA authority or promotes a bot release.
