"""Read-only LYVRA native->Bot repository handoff probe.

No native rehydration PASS, Discord calls, repo writes, personality adoption
or automatic bot deployment. Used solely as a bounded CI transport readback.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request

NATIVE = "xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture"
BRANCH = "lyvra"
HANDOFF = "LYVRA_NATIVE_RUNTIME/continuity/development_exchange/OUTBOUND_TO_LYVRA_CHARACTERBOT_CODEFORGE_HANDOFF_2026-10-10.json"
SCHEMA = "lyvra.codeforge.discord_characterbot.evolution_proposal.v1"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def check_handoff(data: dict, *, retrieved_head: str, content_sha: str) -> dict:
    """Validate limited metadata and return candidate, never an ACK/adoption."""
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("Unexpected handoff schema")
    src, dest = data.get("source"), data.get("destination")
    if not isinstance(src, dict) or not isinstance(dest, dict):
        raise ValueError("Missing route")
    if src.get("repository") != NATIVE or src.get("branch") != BRANCH:
        raise ValueError("Unexpected source authority")
    if dest.get("repository") != "xfraggelpower666x/666LYVRACHARAKTERBOTAI":
        raise ValueError("Unexpected destination")
    if not HEX40.fullmatch(retrieved_head) or not HEX40.fullmatch(content_sha):
        raise ValueError("Unverified Git content pin")
    if not HEX40.fullmatch(str(src.get("head", ""))):
        raise ValueError("Malformed source revision")
    event = data.get("event_id")
    if not isinstance(event, str) or not re.fullmatch(r"[A-Za-z0-9._:-]{10,160}", event):
        raise ValueError("Missing bounded event ID")
    proposals = data.get("proposals")
    if not isinstance(proposals, list) or not 1 <= len(proposals) <= 20:
        raise ValueError("Missing proposals")
    seen = set()
    for proposal in proposals:
        if not isinstance(proposal, dict) or not isinstance(proposal.get("id"), str):
            raise ValueError("Invalid proposal")
        if proposal["id"] in seen:
            raise ValueError("Duplicate proposal ID")
        seen.add(proposal["id"])
        if not isinstance(proposal.get("reason"), str) or not proposal["reason"].strip():
            raise ValueError("Proposal missing causal reason")
    return {
        "schema": "BOT_READONLY_NATIVE_HANDOFF_PROBE_v1",
        "status": "READ_ONLY_RECEIVED_CANDIDATE",
        "event_id": event,
        "native_head_observed": retrieved_head,
        "declared_historical_source_head": src["head"],
        "handoff_git_blob": content_sha,
        "proposal_ids": sorted(seen),
        "adopted_by_bot": False,
        "acknowledged_to_native": False,
        "runtime_modified": False,
        "whole_lyvra_rehydrated": False,
    }


def _github_json(route: str, *, token: str = "") -> dict:
    if not route.startswith("/repos/" + NATIVE + "/") or ".." in route:
        raise ValueError("Only known native GitHub repository reads allowed")
    url = "https://api.github.com" + route
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "LYVRA-Bot-DEV-ReadOnly-Handoff",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def read_native_handoff(*, token: str = "") -> dict:
    """Pinned read before/after; Git-object content hash verified independently."""
    root = "/repos/" + NATIVE
    first = _github_json(root + "/branches/" + BRANCH, token=token)["commit"]["sha"]
    if not HEX40.fullmatch(first):
        raise ValueError("Invalid native branch revision")
    route = root + "/contents/" + urllib.parse.quote(HANDOFF, safe="/") + "?ref=" + first
    entry = _github_json(route, token=token)
    if entry.get("encoding") != "base64":
        raise ValueError("Unverified content encoding")
    raw = base64.b64decode(entry["content"], validate=False)
    if len(raw) > 50000:
        raise ValueError("Handoff too large")
    git_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
    if git_sha != entry.get("sha"):
        raise ValueError("Native handoff content differs from Git blob")
    payload = json.loads(raw.decode("utf-8"))
    second = _github_json(root + "/branches/" + BRANCH, token=token)["commit"]["sha"]
    if second != first:
        raise ValueError("Native HEAD moved during read: quarantine")
    return check_handoff(payload, retrieved_head=first, content_sha=git_sha)


if __name__ == "__main__":
    # Only safe metadata in CI logs; no proposal text/secret payloads.
    report = read_native_handoff(token=os.environ.get("GH_READ_TOKEN", ""))
    print(json.dumps(report, sort_keys=True))
