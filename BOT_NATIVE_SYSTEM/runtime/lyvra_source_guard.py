"""Strict read-only intake of LYVRA source claims for the bot.
SOURCE is never DELIVERY, ADOPTION, HOST or identity authorization.
"""
from __future__ import annotations
from dataclasses import dataclass
import re

SHA = re.compile(r"^[0-9a-f]{40}$")
LYVRA_REPO = "xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture"
LYVRA_BRANCH = "lyvra"

def assess_lyvra_source(envelope: dict, *, observed_lyvra_head: str) -> dict:
    failures = []
    if not isinstance(envelope, dict):
        return {"status": "BLOCKED", "failures": ["INVALID_ENVELOPE"], "source": False,
                "delivery": False, "adoption": False, "host": False}
    if envelope.get("repository") != LYVRA_REPO or envelope.get("branch") != LYVRA_BRANCH:
        failures.append("FOREIGN_AUTHORITY_MISMATCH")
    if not SHA.fullmatch(str(observed_lyvra_head)):
        failures.append("INVALID_OBSERVED_HEAD")
    if not SHA.fullmatch(str(envelope.get("source_head", ""))):
        failures.append("INVALID_SOURCE_SHA")
    if envelope.get("source_head") != observed_lyvra_head:
        failures.append("STALE_SOURCE")
    if envelope.get("identity_authority") != "WHOLE_LYVRA":
        failures.append("IDENTITY_AUTHORITY_MISMATCH")
    return {"status": "BLOCKED" if failures else "SOURCE_ONLY",
            "failures": failures, "source": not failures,
            "delivery": False, "adoption": False, "host": False,
            "native_lyvra_worker_writes": False,
            "bot_identity_authority": False}
