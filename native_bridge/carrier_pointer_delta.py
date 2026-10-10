"""Compare public LYVRA pointer facets, without promotion or native writes."""
import hashlib
import json
from native_bridge.carrier_evolution import candidates_from_pointer

def compare_pointers(previous, current, previous_head, current_head):
    old = candidates_from_pointer(previous, previous_head)
    new = candidates_from_pointer(current, current_head)
    result = []
    for left, right in zip(old["surfaces"], new["surfaces"]):
        if left["surface"] != right["surface"]:
            raise ValueError("Facet mismatch")
        before = json.dumps(left["pointer_fields"], sort_keys=True, default=str)
        after = json.dumps(right["pointer_fields"], sort_keys=True, default=str)
        if before != after:
            result.append({"surface": right["surface"],
                           "status": "REVIEW_CANDIDATE",
                           "old_sha256": hashlib.sha256(before.encode()).hexdigest(),
                           "new_sha256": hashlib.sha256(after.encode()).hexdigest(),
                           "integration_verified": False})
    return {"schema": "LYVRA_CARRIER_POINTER_DELTA_v1",
            "previous_head": previous_head, "current_head": current_head,
            "changes": result, "native_mutated": False,
            "promotion_authorized": False}
