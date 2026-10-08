"""Compare technical journal source revisions before DEV resumption."""
def resume_gate(record, native_head, carrier_head):
    if record.get("native_mutated") is not False or record.get("production_promoted") is not False:
        raise ValueError("Unsafe record")
    fresh=(record.get("native_head")==native_head and
           record.get("carrier_head")==carrier_head)
    return {"schema":"LYVRA_CARRIER_RESUME_GATE_v1",
            "status":"REVIEW_CANDIDATE" if fresh else "REFRESH_REQUIRED",
            "fresh":fresh,"native_modified":False,
            "restored":False,"deployment_authorized":False}
