"""Read-only evidence contract collector for the LYVRA carrier.

Consumes explicit path and expected blob SHA supplied by current manifests.
Never upgrades pointer labels to proof, never reads private payloads, and
never writes Native/Discord/production files.
"""
from __future__ import annotations
import hashlib
import re
from native_bridge.carrier_compatibility import SURFACES

SHA = re.compile(r"^[0-9a-f]{40}$")
PREFIXES = ("LYVRA_NATIVE_RUNTIME/", "LYVRA_PET/")

def collect(source, head, contracts):
    if not isinstance(head, str) or not SHA.fullmatch(head):
        raise ValueError("Invalid pinned native HEAD")
    results = {}
    for surface in SURFACES:
        items = contracts.get(surface, ())
        verified = []
        blockers = []
        for item in items:
            path = item.get("path", "")
            expected = item.get("blob_sha", "")
            if (not isinstance(path, str) or not path.startswith(PREFIXES)
                    or ".." in path.split("/") or not SHA.fullmatch(str(expected))
                    or any(part.startswith(".") for part in path.split("/"))):
                blockers.append("INVALID_CONTRACT_REFERENCE")
                continue
            try:
                body = source.read(path, head)
                raw = body.encode("utf-8")
                actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
                if actual != expected:
                    blockers.append("BLOB_MISMATCH")
                    continue
                verified.append({"path": path, "blob_sha": actual})
            except (OSError, ValueError, UnicodeError, KeyError):
                blockers.append("READBACK_FAILED")
        results[surface] = {
            "status": "CONTRACTS_READ" if verified and not blockers else "READBACK_PENDING",
            "evidence": verified, "blockers": blockers,
            "compatible": False, "whole_rehydration": False,
        }
    return {"schema": "LYVRA_CARRIER_CONTRACT_READBACK_v1",
            "native_head": head, "results": results,
            "native_mutation": False, "deployment": False}
