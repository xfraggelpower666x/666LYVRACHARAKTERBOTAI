# Stage 23 — Stream tee cancellation fix

STATUS=SOURCE_READBACK_PASS / ISOLATED_NODE_REPRODUCER_VERIFIED / COMPLETE_CI_UNVERIFIED / PRODUCTION_BLOCKED
BASE_HEAD=f19cef5197e6da1244d732c898a0fe3d31d6e2e8
CODE_HEAD=4fc8655c02096d447095b5e5c82983350b57f278

Node.js 22.16.0 local reproduction: await reader.cancel() on a cloned Request tee with unread sibling timed out after 300 ms. Nonawaited cancellation with immediate reader.releaseLock completed without blocking in an isolated check. Source modified to prevent awaiting this cancellation for oversized Discord requests. Added timeout-based regression case and forged-short-Content-Length streaming test. Source and tests read back from GitHub using exact branch blobs. This does not constitute execution of the complete checked-in Node test suite or GitHub Actions CI.

No Cloudflare deployment, no D1 provisioning, no billing changes, no native LYVRA, CLIC, PET or STREAM writes. Default-off worker state remains from previous Cloudflare readback; not freshly independently rechecked in this stage. Native approval, CI and zero-cost billing evidence pending.
