"""Read-only, evidence-separated LYVRA carrier compatibility analysis.

Never rehydrates native LYVRA, changes identity, deploys or writes to GitHub.
Inputs are caller-supplied evidence snapshots; missing evidence stays OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Mapping
import json

SURFACES = (
    "native_identity", "personality_livecircle", "music_speech",
    "website", "dashboard", "visual_intelligence", "plugin_native",
    "plugin_account", "pet",
)
REQUIRED = {
    "native_identity": ("identity", "current_pointer"),
    "personality_livecircle": ("personality_manifest", "privacy_boundary"),
    "music_speech": ("music_contract", "speech_contract"),
    "website": ("website_version", "website_contract"),
    "dashboard": ("dashboard_version", "dashboard_contract"),
    "visual_intelligence": ("visual_manifest", "asset_permissions"),
    "plugin_native": ("native_plugin_version", "skill_contract"),
    "plugin_account": ("account_plugin_version", "skill_contract"),
    "pet": ("pet_manifest", "pet_asset_provenance"),
}

@dataclass(frozen=True)
class Finding:
    surface: str
    status: str
    missing: tuple[str, ...]
    evidence: tuple[str, ...]
    reason: str


def audit(native: Mapping, carrier: Mapping) -> dict:
    """Compare proven surface contracts, not personality contents or guesses.

    Evidence entries are attestations with source SHA and contract fingerprint.
    Merely naming a facet in a README is not proof of its implementation.
    """
    native_head = native.get("head")
    carrier_head = carrier.get("head")
    def valid_sha(s):
        return isinstance(s, str) and len(s) == 40 and all(c in "0123456789abcdef" for c in s)

    if not valid_sha(native_head) or not valid_sha(carrier_head):
        raise ValueError("Both pinned source HEADs must be verified SHA-1 refs")
    findings = []
    n_surfaces = native.get("surfaces") or {}
    c_surfaces = carrier.get("surfaces") or {}
    for surface in SURFACES:
        n = n_surfaces.get(surface) or {}
        c = c_surfaces.get(surface) or {}
        required = REQUIRED[surface]
        missing = tuple(k for k in required if not n.get(k))
        evidence = tuple(sorted(set(n.get("evidence") or [])))
        if missing:
            status, reason = "READBACK_PENDING", "Native contract/evidence incomplete"
        elif not n.get("fingerprint") or not evidence:
            status, reason = "READBACK_PENDING", "Missing contract fingerprint or provenance"
        elif c.get("native_fingerprint") != n["fingerprint"]:
            status, reason = "ADAPTATION_REVIEW", "Carrier has not attested current native contract"
        elif not c.get("tested") or not c.get("readback"):
            status, reason = "TEST_PENDING", "No test plus remote readback for this carrier contract"
        else:
            status, reason = "COMPATIBLE_DEV", "Version-bound DEV evidence only; not a live deployment"
        findings.append(Finding(surface, status, missing, evidence, reason))
    return {
        "schema": "LYVRA_CARRIER_COMPATIBILITY_v1",
        "native_head": native_head,
        "carrier_head": carrier_head,
        "native_identity_mutation": False,
        "bot_production_mutation": False,
        "whole_rehydration_claim": False,
        "overall": "DEV_REVIEW_ONLY" if all(f.status == "COMPATIBLE_DEV" for f in findings)
                   else "PARTIAL/INTEGRATION_GATES_OPEN",
        "findings": [asdict(f) for f in findings],
    }


def as_report(native: Mapping, carrier: Mapping) -> str:
    """Deterministic machine-readable report; printing does not publish it."""
    return json.dumps(audit(native, carrier), ensure_ascii=False, indent=2, sort_keys=True)
