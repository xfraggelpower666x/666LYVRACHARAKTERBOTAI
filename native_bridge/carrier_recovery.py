"""Read-only recovery planning for the technical LYVRA Carrier journal.

This is NOT native LYVRA rehydration and never restores Discord memory.
Recovery is only a verified plan; no automatic state replacement.
"""
from __future__ import annotations
from native_bridge.carrier_journal_audit import verify_history

def recovery_plan(document, expected_native_head=None):
    check=verify_history(document)
    last=check["last_native_head"]
    if expected_native_head is not None and last != expected_native_head:
        return {"schema":"LYVRA_CARRIER_DEV_RECOVERY_v1",
                "status":"STALE_REFERENCE_REVALIDATE", "records":check["entries"],
                "last_native_head":last,"restored":False,"native_mutated":False}
    return {"schema":"LYVRA_CARRIER_DEV_RECOVERY_v1",
            "status":"RECOVERY_CANDIDATE_VERIFIED",
            "records":check["entries"],"last_native_head":last,
            "restored":False,"native_mutated":False,
            "deployment_authorized":False}
