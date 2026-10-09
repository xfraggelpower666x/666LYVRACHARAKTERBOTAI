# Validation & release acceptance matrix

DOCS_CREATED != RUNTIME_IMPLEMENTED.
Acceptance must independently prove:
- branch and repository history readback
- schema-valid bot manifest/pointer and exact version scope
- Python syntax + offline tests for native_bridge and automation
- Discord hardlock inability to reach bot.run without both verified gates
- bot-specific Worker challenge, signature verification, nonce, expiry, replay/revocation, audience and network-failure tests
- recipient-authorized native LYVRA handoff receipt before any LYVRA worker mutation
- independently tested Discord test guild with consent and least-privilege scopes
- independent family/radio/Verba nonmutation and protected recovery
- versioned release plus separate production approval

For the initial native-system folder: **documentation and repository identity only**. All other acceptance gates remain pending unless separately tested.
