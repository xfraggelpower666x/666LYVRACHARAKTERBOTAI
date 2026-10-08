"""DEV-only carrier evolution journal and existing watcher topic bridge.

Consumes existing path-classifier as *hint*, never as a verified native fact.
Journal stores hashes/statuses only; no personality, relationship or chat payloads.
No native/bot production writes, automatic promotion or GitHub Issue edits.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from native_bridge.carrier_evolution import candidates_from_pointer
from native_bridge.carrier_compatibility import audit

SCHEMA = "LYVRA_CARRIER_DEV_JOURNAL_v1"
ALLOWED = {"REVIEW_CANDIDATE", "READBACK_PENDING", "ADAPTATION_REVIEW",
           "TEST_PENDING", "COMPATIBLE_DEV"}


def watcher_topics(changed_paths, classifier):
    """Reuse existing native_update_todos.classify_path without changing it."""
    return sorted({topic for path in changed_paths for topic in classifier(path)})


def build_record(native_head, bot_head, pointer, changed_paths, classifier):
    candidates = candidates_from_pointer(pointer, native_head)
    # Candidate metadata is not evidence of native contract parity.
    results = audit({"head": native_head, "surfaces": {}},
                    {"head": bot_head, "surfaces": {}})
    topics = watcher_topics(changed_paths, classifier)
    surfaces = [
        {"surface": item["surface"], "status": item["status"],
         "missing_fields": item["missing_fields"]}
        for item in candidates["surfaces"]
    ]
    return {"schema": SCHEMA, "native_head": native_head, "carrier_head": bot_head,
            "topics": topics, "surfaces": surfaces, "compatibility": results["overall"],
            "native_mutated": False, "production_promoted": False,
            "whole_rehydration_claim": False}


def record_digest(record):
    raw = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def append_local_journal(path, record):
    """Explicit DEV-only local persistence. Never writes repository/native state.

    Existing history preserved; duplicate snapshots idempotent. Path must sit
    underneath a caller-supplied private local state directory.
    """
    p = Path(path)
    if p.suffix != ".json" or p.name.startswith("."):
        raise ValueError("Journal requires named .json file")
    if record.get("schema") != SCHEMA or record.get("native_mutated") is not False:
        raise ValueError("Invalid journal record")
    if record.get("production_promoted") is not False:
        raise ValueError("Promotion marker forbidden")
    if any(x.get("status") not in ALLOWED for x in record.get("surfaces", [])):
        raise ValueError("Invalid status")
    p.parent.mkdir(parents=True, exist_ok=True)
    previous = []
    if p.exists():
        parsed = json.loads(p.read_text(encoding="utf-8"))
        if parsed.get("schema") != SCHEMA or not isinstance(parsed.get("history"), list):
            raise ValueError("Unknown journal schema: refuse overwrite")
        from native_bridge.carrier_journal_audit import verify_history
        verify_history(parsed)
        previous = parsed["history"]
    digest = record_digest(record)
    if any(entry.get("digest") == digest for entry in previous):
        return False
    history = previous + [{"digest": digest, "record": record}]
    data = json.dumps({"schema": SCHEMA, "history": history}, ensure_ascii=False, indent=2)
    temp_path = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(p.parent),
                                prefix=".carrier-", suffix=".tmp", delete=False) as f:
            temp_path = f.name
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, p)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
    return True
