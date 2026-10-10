"""Local, opt-in, fail-closed handoff outbox for public-safe review candidates.

Not a Discord listener, network client, automatic publisher or LYVRA memory.
Content-level privacy/consent review MUST precede calling this module.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

from native_bridge.reciprocal_learning import SCHEMA, prepare_candidate, validate_receipt

_EVENT = re.compile(r"^bot2native-[0-9a-f]{64}$")


def _safe_dir(root):
    p = Path(root)
    if not p.is_absolute() or p.is_symlink() or p.exists() and not p.is_dir():
        raise ValueError("Outbox root must be an absolute, non-symlink directory")
    # Keep outbox under a caller-controlled private path, never auto-select repo path.
    p.mkdir(parents=True, exist_ok=True)
    if p.is_symlink():
        raise ValueError("Symlinked outbox root forbidden")
    return p


def _write_once(target, obj):
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if target.is_symlink():
        raise ValueError("Symlink destination forbidden")
    try:
        with target.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        return "STORED_LOCAL_ONLY"
    except FileExistsError:
        if target.is_symlink() or target.read_bytes() != data:
            raise ValueError("Conflicting event file; no overwrite permitted")
        return "ALREADY_STORED_IDENTICAL"


def queue_review_candidate(private_outbox_root, payload, *, privacy_reviewed=False):
    """Store only a caller-reviewed event, never send it to either repo."""
    if privacy_reviewed is not True:
        raise ValueError("Content-level privacy review is mandatory")
    candidate = prepare_candidate(payload)
    event = candidate["event_id"]
    if not _EVENT.fullmatch(event) or candidate["schema"] != SCHEMA:
        raise ValueError("Invalid content-addressed candidate")
    directory = _safe_dir(private_outbox_root)
    dest = directory / (event + ".json")
    status = _write_once(dest, candidate)
    return {"event_id": event, "status": status, "location": str(dest),
            "network_sent": False, "native_adopted": False}


def review_receipt(candidate, receipt, *, verified_native_readback=None):
    """Return verification classification without storing or promoting native state."""
    if candidate.get("schema") != SCHEMA or candidate.get("status") != "NATIVE_REVIEW_PENDING":
        raise ValueError("Unknown candidate state")
    result = validate_receipt(receipt, candidate["event_id"],
                              verified_native_readback=verified_native_readback)
    return {"event_id": candidate["event_id"], "decision": result["decision"],
            "status": result["status"], "native_adopted": result["native_adopted"],
            "delivery_confirmed": False, "whole_lyvra_only": True}
