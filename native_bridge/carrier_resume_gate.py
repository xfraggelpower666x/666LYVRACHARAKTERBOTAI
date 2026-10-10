"""Fail-closed technical carrier resume against pinned native and bot commits."""
import re
SHA = re.compile(r"^[0-9a-f]{40}$")
def resume_gate(record, native_head, carrier_head):
    if not isinstance(record, dict):
        raise ValueError("Invalid record")
    if not all(isinstance(x, str) and SHA.fullmatch(x) for x in (native_head, carrier_head)):
        raise ValueError("Unpinned source commits")
    if record.get("native_mutated") is not False or record.get("production_promoted") is not False:
        raise ValueError("Unsafe record")
    if record.get("identity_authority", "NATIVE_LYVRA_ONLY") != "NATIVE_LYVRA_ONLY":
        raise ValueError("Foreign identity authority")
    fresh = record.get("native_head") == native_head and record.get("carrier_head") == carrier_head
    return {"schema": "LYVRA_CARRIER_RESUME_GATE_v1",
            "status": "REVIEW_CANDIDATE" if fresh else "REFRESH_REQUIRED",
            "fresh": fresh, "native_modified": False,
            "restored": False, "deployment_authorized": False}
