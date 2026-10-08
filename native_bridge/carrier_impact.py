"""Deterministic causal impact triage for LYVRA carrier development.

Path matches are hypotheses, never proof. No automatic code change, identity
mutation, live learning, protected reads, promotions or deployment.
"""
from __future__ import annotations

DEPENDENCIES = {
    "native_identity": ("personality_livecircle", "pet", "visual_intelligence"),
    "personality_livecircle": ("pet", "website"),
    "music_speech": ("pet", "website", "visual_intelligence"),
    "visual_intelligence": ("dashboard", "pet"),
    "plugin_native": ("dashboard", "pet"),
    "plugin_account": ("dashboard", "pet"),
    "website": ("dashboard",),
    "dashboard": (),
    "pet": (),
}
RISK_ORDER = ("BLOCKED", "DIRECT_REVIEW", "DEPENDENCY_REVIEW", "NO_CHANGE_EVIDENCE")


def triage(findings, changed_surfaces, *, native_head, bot_head):
    """Produce bounded explanations of possible causal dependencies.

    Input must be attested elsewhere. An observed difference is NOT a
    demonstrated cause; dependent surfaces are nominated for review only.
    """
    if not isinstance(findings, list):
        raise ValueError("Findings must be a list")
    known = set(DEPENDENCIES)
    changed = set(changed_surfaces)
    if changed - known:
        raise ValueError("Unknown surface; fail closed")
    if not all(isinstance(s, str) and len(s) == 40 and
               all(c in "0123456789abcdef" for c in s)
               for s in (native_head, bot_head)):
        raise ValueError("Pinned SHAs required")
    by_surface = {f["surface"]: f for f in findings if f.get("surface") in known}
    if len(by_surface) != len(findings) or set(by_surface) != known:
        raise ValueError("Incomplete or duplicated compatibility findings")
    affected = set(changed)
    frontier = list(sorted(changed))
    reasons = {s: ["Source surface changed; causal relevance unverified"] for s in changed}
    while frontier:
        source = frontier.pop(0)
        for target in DEPENDENCIES[source]:
            reasons.setdefault(target, []).append("Possible dependency from " + source)
            if target not in affected:
                affected.add(target)
                frontier.append(target)
    result = []
    for surface in DEPENDENCIES:
        status = by_surface[surface]["status"]
        if status not in {"COMPATIBLE_DEV", "TEST_PENDING", "READBACK_PENDING", "ADAPTATION_REVIEW"}:
            raise ValueError("Unexpected compatibility status")
        classification = ("BLOCKED" if status == "READBACK_PENDING" else
                          "DIRECT_REVIEW" if surface in changed else
                          "DEPENDENCY_REVIEW" if surface in affected else
                          "NO_CHANGE_EVIDENCE")
        result.append({"surface": surface, "impact": classification,
                       "compatibility": status, "reason": sorted(set(reasons.get(surface, []))),
                       "promotion_allowed": False})
    return {"schema": "LYVRA_CARRIER_CAUSAL_IMPACT_v1",
            "native_head": native_head, "carrier_head": bot_head,
            "causality": "HYPOTHESIS_NOT_PROVEN",
            "native_mutation": False, "automatic_adapter_mutation": False,
            "findings": result}
