# Cloudflare-only: zero additional costs
DATE=2026-10-10
STATUS=CREATOR_HARD_REQUIREMENT
CLOUDFLARE_ONLY=true
ZERO_ADDITIONAL_COST=true
NO_PAID_UPGRADE=true
NO_PAID_EXTERNAL_AI=true
DISCORD_INTERACTIONS_HTTP_FIRST=true
LONG_LIVED_GATEWAY_UNPROVEN=true
VOICE_RUNTIME_UNPROVEN=true
LYVRA_NATIVE_AUTHORITY_UNCHANGED=true

Use exclusively existing Cloudflare hosting within verified no-extra-cost quotas. Never provision billable products or automatically upgrade plans. Prefer Discord HTTP Interactions with Ed25519 verification, bounded execution, separate own bot authorization and explicit fail-closed behavior. Standard Workers are not assumed to run a persistent Python Discord Gateway session or voice connection. Evaluate D1 only after quotas and account plan are checked. GitHub retains source/receipts, not bot compute. Native LYVRA-owned Workers must not be changed without verified native repository handoff approval. Preserve the current DISCORD_OFFLINE gate until real end-to-end tests, abuse safeguards, deployment identity and measured usage pass.

References: https://developers.cloudflare.com/workers/platform/limits/ and https://developers.cloudflare.com/workers/platform/pricing/