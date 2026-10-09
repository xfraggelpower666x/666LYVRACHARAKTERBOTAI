"""Bot-owned offline continuity and direct-command parsing. No Discord or network IO."""
from __future__ import annotations
import re
from typing import Any

SYSTEM_ID = "666LYVRA-CHARACTER-BOT-CORE-001"
PREFIX = re.compile(r"^\s*(?:666LYVRABOT|666\s+LYVRA\s+BOT)\s+(SYSTEMSTART|WEITER|UPDATE|DASHBOARD|AUDIT|CODEFORGE|HANDOFF|RECOVERY|FACETS|CAPABILITIES|NEW CHAT|NEXT CHAT)\s*$", re.I)
SHA = re.compile(r"^[a-f0-9]{40}$")
RELATIONS = frozenset({"KEEP_ACTIVE", "KEEP_REACHABLE", "ARCHIVE", "SUPERSEDE", "REJECT_WITH_PROVENANCE", "REACTIVATE_WHEN_CAUSALLY_RELEVANT"})

def parse_direct_trigger(message: str, *, direct_user_message: bool) -> str | None:
    if not direct_user_message or not isinstance(message, str):
        return None
    match = PREFIX.fullmatch(message)
    return match.group(1).upper() if match else None

def validate_system(manifest: dict[str, Any], pointer: dict[str, Any]) -> dict[str, Any]:
    blockers = []
    if manifest.get("system_id") != SYSTEM_ID:
        blockers.append("IDENTITY_MISMATCH")
    if manifest.get("status") != "DEV_NOT_PROMOTED":
        blockers.append("UNEXPECTED_MANIFEST_STATE")
    if pointer.get("schema") != "BOT_CURRENT_POINTER_v1":
        blockers.append("POINTER_SCHEMA_MISMATCH")
    if pointer.get("status") != "DEV_CANDIDATE_ONLY":
        blockers.append("UNEXPECTED_POINTER_STATE")
    if not SHA.fullmatch(str(pointer.get("source_baseline_commit", ""))):
        blockers.append("INVALID_BASELINE_SHA")
    if manifest.get("discord_login_allowed") is not False or pointer.get("discord_deployment") is not False:
        blockers.append("DISCORD_NOT_LOCKED")
    if manifest.get("lyvra_worker_writes_allowed") is not False:
        blockers.append("FOREIGN_WORKER_WRITE_RISK")
    if pointer.get("runtime_head_selected") is not False:
        blockers.append("UNPROVEN_RUNTIME_PROMOTION")
    return {"status": "STRUCTURE_PASS" if not blockers else "BLOCKED", "blockers": blockers,
            "release_ready": False, "native_lyvra_authority": False}

def validate_event(event: dict[str, Any]) -> list[str]:
    problems = []
    required = ("event_id", "timestamp_utc", "facet", "source_ref", "source_sha", "cause", "decision", "effects", "validation", "relation", "supersedes", "rollback_ref")
    for k in required:
        if k not in event:
            problems.append("MISSING_" + k.upper())
    if event.get("relation") not in RELATIONS:
        problems.append("INVALID_RELATION")
    if not SHA.fullmatch(str(event.get("source_sha", ""))):
        problems.append("INVALID_SOURCE_SHA")
    return problems
