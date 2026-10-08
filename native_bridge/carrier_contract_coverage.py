"""Strict bridge from verified native blob references to compatibility evidence.

Blob integrity proves bytes at a pinned ref, not behavioral compatibility.
Only caller-supplied explicit contract mappings are eligible. No mutation.
"""
from __future__ import annotations
from native_bridge.carrier_compatibility import SURFACES, REQUIRED, audit

def summarize_contract_coverage(readback, native_head, bot_head):
    if readback.get("native_head") != native_head:
        raise ValueError("Native HEAD mismatch: reject stale evidence")
    results = readback.get("results", {})
    output = {}
    for surface in SURFACES:
        item = results.get(surface, {})
        evidence = item.get("evidence", ())
        verified = item.get("status") == "CONTRACTS_READ"
        output[surface] = {
            "status": "BLOB_READBACK_VERIFIED" if verified else "READBACK_PENDING",
            "blob_evidence": [dict(path=e["path"], blob_sha=e["blob_sha"]) for e in evidence]
                             if verified else [],
            "missing_behavioral_proofs": list(REQUIRED[surface]),
            "compatibility_confirmed": False,
        }
    compatible = audit({"head": native_head, "surfaces": {}},
                       {"head": bot_head, "surfaces": {}})
    return {"schema": "LYVRA_CARRIER_CONTRACT_COVERAGE_v1",
            "native_head": native_head, "carrier_head": bot_head,
            "surfaces": output, "compatibility": compatible["overall"],
            "deployment_allowed": False, "native_changed": False}
