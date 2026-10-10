"""Offline snapshot of the bot's own provenance ledger; never a native LYVRA boot."""
from rehydration_stage02 import rehydrate
from sqlite_ledger import read

def snapshot(manifest, pointer, observed_head, expected_branch, ledger_path):
    result = rehydrate(manifest, pointer, observed_head, expected_branch)
    if result["status"] == "BLOCKED":
        return {**result, "facets": {}, "events": 0}
    try:
        records = read(ledger_path, set(manifest.get("facets", [])))
    except (ValueError, OSError, RuntimeError) as exc:
        return {**result, "status": "BLOCKED", "blockers": ["LEDGER_READBACK_FAILED"], "facets": {}, "events": 0}
    facets = {f: {"events": 0, "latest_event_id": None} for f in manifest.get("facets", [])}
    for record in records:
        item = facets[record["facet"]]
        item["events"] += 1
        item["latest_event_id"] = record["event_id"]
    return {**result, "facets": facets, "events": len(records), "last_verified_return_anchor": None}
