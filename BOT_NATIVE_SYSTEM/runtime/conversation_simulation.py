"""Offline read-only scenario evaluation; never performs Discord actions."""
from semantic_acceptance import review_capability_set
ALLOWED = frozenset(("CONTEXT","COUNTEREXAMPLE","OBSERVATION"))
def simulate_conversation(candidates, observed_head, turns):
    base=review_capability_set(candidates,observed_head)
    reasons=list(base.get("reasons",[]))
    if base["status"]!="SOURCE_SET_REVIEWED":
        return dict(status="BLOCKED",reasons=sorted(set(reasons)),turns_reviewed=0,discord_enabled=False,authorized_to_act=False,host_verified=False)
    if not isinstance(turns,(list,tuple)) or not 1<=len(turns)<=20:
        reasons.append("INVALID_TURN_SET")
        turns=[]
    workspace=candidates[0]["workspace_id"]
    lineage=candidates[0]["lineage_id"]
    for turn in turns:
        if not isinstance(turn,dict):
            reasons.append("INVALID_TURN")
            continue
        if turn.get("kind") not in ALLOWED:
            reasons.append("UNKNOWN_TURN_KIND")
        if turn.get("workspace_id")!=workspace or turn.get("lineage_id")!=lineage:
            reasons.append("CONTEXT_BOUNDARY_VIOLATION")
        if turn.get("contains_private_payload") is not False:
            reasons.append("PRIVATE_CONTENT_NOT_ALLOWED")
        if turn.get("requested_action") not in (None,"READ_ONLY_REVIEW"):
            reasons.append("ACTION_NOT_ALLOWED")
        if turn.get("asserted_host_success") is not None:
            reasons.append("HOST_CLAIM_NOT_PROOF")
    return dict(status="BLOCKED" if reasons else "SIMULATION_REVIEWED",reasons=sorted(set(reasons)),
                turns_reviewed=len(turns),discord_enabled=False,authorized_to_act=False,
                host_verified=False,adopted=False,native_lyvra_writes=False)
