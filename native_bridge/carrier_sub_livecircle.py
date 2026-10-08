"""DEV carrier sub-LiveCircle: append-only technical snapshots by reference.

Only caller-selected local persistence. No native memories, Discord chats,
private payloads, GitHub issue mutation, or automatic deployment.
"""
from __future__ import annotations
from native_bridge.carrier_delta_pipeline import preview
from native_bridge.carrier_journal import append_local_journal, SCHEMA

def prepare_circle_record(report):
    if report.get("schema") != "LYVRA_CARRIER_DELTA_PIPELINE_v1":
        raise ValueError("Unexpected pipeline schema")
    analysis = report["analysis"]
    delta = report["delta"]
    if report.get("auto_apply") is not False or report.get("deployed") is not False:
        raise ValueError("Unsafe pipeline result")
    record = dict(analysis["journal_candidate"])
    if record.get("schema") != SCHEMA:
        raise ValueError("Incompatible journal schema")
    record["delta"] = [{"surface": x["surface"], "status": x["status"],
                        "old_sha256": x["old_sha256"], "new_sha256": x["new_sha256"]}
                       for x in delta["changes"]]
    record["circle_state"] = "REVIEW_PENDING"
    record["identity_authority"] = "NATIVE_LYVRA_ONLY"
    return record

def persist_dev_report(path, report):
    """Explicit call only: local journal append, never automated in live bot."""
    return append_local_journal(path, prepare_circle_record(report))
