"""Immutable DEV evidence gate for LYVRA carrier facet releases.

Technical contracts only. No LYVRA identity copying, no automatic release,
and no inference of runtime capability from Git blob verification.
"""
from __future__ import annotations
import re
from native_bridge.carrier_compatibility import SURFACES

SHA = re.compile(r"^[a-f0-9]{40}$")

def decision(coverage, compatibility, *, native_head, carrier_head):
    if not all(isinstance(v, str) and SHA.fullmatch(v) for v in (native_head, carrier_head)):
        raise ValueError("Pinned commit SHAs required")
    if coverage.get("native_head") != native_head or coverage.get("carrier_head") != carrier_head:
        raise ValueError("Stale contract coverage")
    if compatibility.get("native_head") != native_head or compatibility.get("carrier_head") != carrier_head:
        raise ValueError("Stale compatibility evidence")
    known = {f.get("surface"): f for f in compatibility.get("findings", ())}
    if set(known) != set(SURFACES) or len(compatibility.get("findings", ())) != len(SURFACES):
        raise ValueError("Incomplete compatibility findings")
    checked = {}
    for surface in SURFACES:
        blob_ok = coverage.get("surfaces", {}).get(surface, {}).get("status") == "BLOB_READBACK_VERIFIED"
        contract_status = known[surface]["status"]
        checked[surface] = {
            "blob_verified": blob_ok,
            "compatibility": contract_status,
            "release_gate": "REVIEW_ONLY" if blob_ok and contract_status == "COMPATIBLE_DEV" else "BLOCKED",
        }
    return {
        "schema": "LYVRA_CARRIER_RELEASE_GATE_v1",
        "native_head": native_head, "carrier_head": carrier_head,
        "surfaces": checked,
        "automatic_promotion": False, "deployment_authorized": False,
        "native_modified": False, "manual_approval_required": True,
    }
