# Carrier integration gate: divergent bot branches

Status: REVIEW_REQUIRED. Scope: bot DEV only.

Verified comparison: DEV branch lyvrabot-dev-native-livecircle-20261002 is 79 commits ahead of lyvrabot and 3 commits behind. The three production-only files are:
- .github/workflows/native-update-todos.yml
- automation/native_update_todos.py
- automation/test_native_update_todos.py

Do not promote or overwrite either branch. Preserve the productive hourly issue-only watcher. Inspect these three files and associated commits before any guarded, conflict-aware integration.

Native LYVRA is the sole identity authority. Bot DEV components may only analyze metadata or explicitly authorized contracts, and must not assert whole rehydration, live Discord readiness, or automatic release.

Acceptance gates: pin both heads; read back current native pointer; reconcile watcher files into a separate reviewable bot-DEV change; offline CI; issue checkbox and checkpoint retention; reviewer acceptance; non-production Discord E2E; recovery proof. No deployment without separate approval.

Evidence: GitHub compare lyvrabot...lyvrabot-dev-native-livecircle-20261002 and reverse comparison, checked 2026-10-08.
