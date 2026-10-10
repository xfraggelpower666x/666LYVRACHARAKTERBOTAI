"""Verify carrier DEV journal continuity before recovery or further learning.

Read-only by default. No private LYVRA state, runtime deployment, native write
or implicit promotion. Existing v1 journals remain readable.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from native_bridge.carrier_journal import SCHEMA, record_digest

def verify_history(document):
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        raise ValueError("Unknown carrier journal schema")
    history = document.get("history")
    if not isinstance(history, list):
        raise ValueError("Malformed journal history")
    seen = set()
    prior_native = None
    for number, entry in enumerate(history):
        if not isinstance(entry, dict) or not isinstance(entry.get("record"), dict):
            raise ValueError("Malformed journal record")
        data = entry["record"]
        digest = entry.get("digest")
        if digest != record_digest(data) or digest in seen:
            raise ValueError("Digest corruption or duplicate at event " + str(number))
        if data.get("schema") != SCHEMA:
            raise ValueError("Record schema mismatch")
        if data.get("native_mutated") is not False or data.get("production_promoted") is not False:
            raise ValueError("Unsafe journal record")
        if data.get("identity_authority", "NATIVE_LYVRA_ONLY") != "NATIVE_LYVRA_ONLY":
            raise ValueError("Identity authority drift")
        seen.add(digest)
        prior_native = data.get("native_head")
    return {"schema": "LYVRA_CARRIER_JOURNAL_AUDIT_v1",
            "entries": len(history), "last_native_head": prior_native,
            "integrity": "PASS", "native_modified": False,
            "promotion_authorized": False}

def readback(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise ValueError("Missing or linked journal")
    return verify_history(json.loads(p.read_text(encoding="utf-8")))
