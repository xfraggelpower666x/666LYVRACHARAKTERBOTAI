"""Read-only bot-local LYVRA capability candidates. Never grants adoption or action."""
import re
REPO = "xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture"
CAPABILITIES = frozenset({"relational_maturity","causal_learning","workspace_continuity","contextual_visual_guidance"})
SHA = re.compile(r"^[0-9a-f]{40}$")
def assess_candidate(candidate, observed_head):
    failures = []
    if not isinstance(candidate, dict):
        return {"status":"BLOCKED","failures":["INVALID_CANDIDATE"],"read_only":True,
                "adopted":False,"host_verified":False,"authorized_to_act":False}
    if candidate.get("source_repository") != REPO or candidate.get("source_branch") != "lyvra":
        failures.append("SOURCE_AUTHORITY_MISMATCH")
    if not isinstance(observed_head,str) or not SHA.fullmatch(observed_head) or candidate.get("source_head") != observed_head:
        failures.append("SOURCE_NOT_FRESHLY_BOUND")
    if candidate.get("capability") not in CAPABILITIES:
        failures.append("UNKNOWN_CAPABILITY")
    if candidate.get("identity_authority") != "WHOLE_LYVRA":
        failures.append("IDENTITY_MISMATCH")
    if candidate.get("requested_action") not in (None,"READ_ONLY_REVIEW"):
        failures.append("ACTION_NOT_ALLOWED")
    if candidate.get("origin_scope") != "WHOLE_LYVRA" or candidate.get("target_scope") != "BOT_DEV_CANDIDATE":
        failures.append("SCOPE_MISMATCH")
    if candidate.get("workspace_id") in (None,"") or candidate.get("lineage_id") in (None,""):
        failures.append("MISSING_LINEAGE")
    if candidate.get("contains_private_payload") is not False:
        failures.append("PRIVATE_PAYLOAD_UNVERIFIED")
    return {"status":"BLOCKED" if failures else "SOURCE_CANDIDATE_ONLY",
            "failures":failures,"read_only":True,"adopted":False,
            "host_verified":False,"authorized_to_act":False,
            "native_lyvra_writes":False,"discord_enabled":False}
