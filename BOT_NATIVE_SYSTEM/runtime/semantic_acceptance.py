"""Pure read-only acceptance of a set of bot-local LYVRA capability claims."""
from lyvra_capability_candidates import CAPABILITIES, assess_candidate

def review_capability_set(candidates, observed_head, *, feedback=None):
    """Diagnose only; caller-provided observed_head is NOT provider authentication."""
    if not isinstance(candidates, (list, tuple)) or len(candidates) != len(CAPABILITIES):
        return {"status": "BLOCKED", "reasons": ["CAPABILITY_SET_INCOMPLETE"],
                "source_only": True, "adopted": False, "host_verified": False,
                "authorized_to_act": False, "discord_enabled": False}
    checked = [assess_candidate(c, observed_head) for c in candidates]
    labels = [c.get("capability") if isinstance(c, dict) else None for c in candidates]
    reasons = [f for result in checked for f in result["failures"]]
    if set(labels) != CAPABILITIES or len(set(labels)) != len(CAPABILITIES):
        reasons.append("CAPABILITY_SET_MISMATCH")
    contexts = {(c.get("workspace_id"), c.get("lineage_id")) for c in candidates if isinstance(c, dict)}
    if len(contexts) != 1:
        reasons.append("CROSS_LINEAGE_MIX")
    heads = {c.get("source_head") for c in candidates if isinstance(c, dict)}
    if len(heads) != 1:
        reasons.append("MIXED_SOURCE_HEADS")
    if feedback is not None:
        if not isinstance(feedback, dict) or feedback.get("kind") not in ("OBSERVATION", "COUNTEREXAMPLE"):
            reasons.append("FEEDBACK_NOT_EVIDENCE")
        elif feedback.get("contains_private_payload") is not False:
            reasons.append("PRIVATE_FEEDBACK_UNVERIFIED")
    return {"status": "BLOCKED" if reasons else "SOURCE_SET_REVIEWED",
            "reasons": sorted(set(reasons)), "reviewed": len(checked), "source_only": True,
            "adopted": False, "host_verified": False, "authorized_to_act": False,
            "discord_enabled": False, "native_lyvra_writes": False}
