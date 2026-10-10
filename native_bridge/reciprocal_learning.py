"""Offline validation of BOT -> native LYVRA learning candidates.

Pure functions only. No Discord API, network, file writes, memory mutation,
release promotion or native authority. Proposals never become identity.
"""
from __future__ import annotations

import hashlib
import json
import re

SCHEMA = "LYVRA_BOT_TO_NATIVE_LEARNING_CANDIDATE_v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_SOURCES = frozenset({
    "AGGREGATE_FEEDBACK", "OBSERVED_PATTERN", "VERIFIED_PUBLIC_FACT",
    "EXPERIMENT_RESULT", "CREATIVE_IDEA", "TECHNICAL_REGRESSION",
})
ALLOWED_PRIVACY = frozenset({"PUBLIC_SAFE", "CONSENTED_REDACTED_AGGREGATE"})
FORBIDDEN_FIELDS = frozenset({
    "raw_message", "message_content", "chat_history", "transcript",
    "voice_recording", "discord_user_id", "discord_token", "email",
    "secret", "private_memory", "personal_profile", "relationship_history",
    "username", "author_id", "dm_content", "member_id",
})
REQUIRED_STRINGS = (
    "bot_head", "native_head_observed", "source_type",
    "observation", "causal_relevance", "evidence_class",
    "provenance", "uncertainty", "suggested_native_target",
    "suggested_test", "privacy_class",
)


def _reject_protected_fields(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_FIELDS:
                raise ValueError("Protected user data field forbidden")
            _reject_protected_fields(item)
    elif isinstance(value, list):
        for item in value:
            _reject_protected_fields(item)


def prepare_candidate(payload: dict) -> dict:
    """Validate explicitly sanitized, bounded input and return review-only envelope."""
    if not isinstance(payload, dict):
        raise ValueError("Payload must be an object")
    _reject_protected_fields(payload)
    unknown = set(payload) - set(REQUIRED_STRINGS) - {"consent_verified"}
    if unknown:
        raise ValueError("Unexpected fields: " + ", ".join(sorted(unknown)))
    for key in REQUIRED_STRINGS:
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            raise ValueError(f"Missing or invalid {key}")
        if len(payload[key]) > 1500:
            raise ValueError(f"Oversized {key}")
    if not SHA40.fullmatch(payload["bot_head"]) or not SHA40.fullmatch(payload["native_head_observed"]):
        raise ValueError("Pinned GitHub commit hashes required")
    if payload["source_type"] not in ALLOWED_SOURCES:
        raise ValueError("Unsupported learning source")
    if payload["privacy_class"] not in ALLOWED_PRIVACY:
        raise ValueError("Protected or unclassified data prohibited")
    if payload["privacy_class"] == "CONSENTED_REDACTED_AGGREGATE" and payload.get("consent_verified") is not True:
        raise ValueError("Consent evidence required for redacted aggregate")
    if payload.get("consent_verified") not in (None, True, False):
        raise ValueError("Invalid consent marker")
    canonical = {key: payload[key].strip() for key in REQUIRED_STRINGS}
    canonical["consent_verified"] = payload.get("consent_verified") is True
    digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, ensure_ascii=False,
                                        separators=(",", ":")).encode("utf-8")).hexdigest()
    return {
        "schema": SCHEMA,
        "event_id": "bot2native-" + digest,
        "direction": "BOT_TO_NATIVE",
        "source": "BOT_DEV_SANITIZED_PROPOSAL",
        "proposal": canonical,
        "status": "NATIVE_REVIEW_PENDING",
        "identity_authority": "WHOLE_LYVRA_ONLY",
        "native_adopted": False,
        "discord_deployed": False,
        "requires_full_native_readback": True,
    }


def validate_receipt(receipt: dict, event_id: str, *, verified_native_readback=None) -> dict:
    """Classify a bot-provided receipt without trusting its self-attested PASS.

    The verifier is a caller-supplied independently executed native GitHub
    readback with a pinned commit SHA and confirmed matched content. A boolean
    inside the untrusted receipt NEVER establishes native adoption.
    """
    if not isinstance(receipt, dict) or receipt.get("event_id") != event_id:
        raise ValueError("Mismatched event receipt")
    decision = receipt.get("decision")
    if decision not in ("ACK", "DEFER", "REJECT", "ADOPTED"):
        raise ValueError("Unknown receipt decision")

    commit = receipt.get("native_adoption_commit")
    if decision == "ADOPTED":
        if not isinstance(commit, str) or not SHA40.fullmatch(commit):
            raise ValueError("Native adoption report requires pinned commit")
        if verified_native_readback is not None:
            if (not isinstance(verified_native_readback, dict)
                    or verified_native_readback.get("source") != "INDEPENDENT_NATIVE_GITHUB_READBACK"
                    or verified_native_readback.get("commit") != commit
                    or verified_native_readback.get("event_id") != event_id
                    or verified_native_readback.get("matched") is not True):
                raise ValueError("Independent native readback evidence inconsistent")

    confirmed = decision == "ADOPTED" and isinstance(verified_native_readback, dict) and (
        verified_native_readback.get("source") == "INDEPENDENT_NATIVE_GITHUB_READBACK"
        and verified_native_readback.get("commit") == commit
        and verified_native_readback.get("event_id") == event_id
        and verified_native_readback.get("matched") is True
    )
    return {
        "event_id": event_id, "decision": decision,
        "native_adopted": confirmed,
        "status": "NATIVE_ADOPTION_READBACK_VERIFIED" if confirmed
                  else ("ADOPTION_REPORTED_READBACK_PENDING" if decision == "ADOPTED"
                        else "BOT_RECEIPT_ONLY"),
        "receipt_syntax_valid": True,
        "independent_readback_performed_here": False,
    }
