# CodeForge — technical Bot development engine

Purpose: deterministic software delivery for this repository, not a new LYVRA CodeForge identity.

Stages: (1) AUDIT current HEAD and contracts; (2) PLAN minimal changes with impacts; (3) RECOVERY save prechange baseline; (4) IMPLEMENT only in authorized bot scope; (5) VALIDATE syntax/unit/privacy/no-login gates; (6) READBACK actual changed blobs and commit SHA; (7) FREEZE verified result and append LifeCircle evidence; (8) RELEASE only with separate explicit approval.

Always perform dry-run diff/conflict checks and preserve two original branches. No uncontrolled `rsync --delete`, `force push`, branch deletion, hidden triggering of historical import workflow, automatic merge to `lyvrabot`, or secret printing. Never alter `lyvrasystem`, PET workers, radio bots, native LYVRA repos or secret bindings from a bot system update.

Development scoreboard uses actual counts (completed vs total verified tasks), no fabricated percentage. An offline unit test is not Discord E2E; presence of a source contract is not an approved handoff.
