"""Passive LYVRA native-repository delta -> Discord Bot integration TODO.

This is a metadata watcher, NOT a native rehydration, bot updater or router.
- Reads public GitHub changes in native *productive* lyvra branch.
- Appends review candidates to a persistent bot-repository GitHub issue.
- Never downloads private runtime state; never publishes source file contents.
- Never edits code, labels, checked TODOs, bot deployments or native pointers.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

NATIVE = "xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture"
BOT = "xfraggelpower666x/666LYVRACHARAKTERBOTAI"
ISSUE = 2
NATIVE_BRANCH = "lyvra"
MARKER_RE = re.compile(r"<!-- LYVRA_NATIVE_HEAD:([0-9a-f]{40}) -->")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def api(route: str, *, token: str = "", payload: object | None = None):
    if not route.startswith("/repos/") or any(part in (".", "..") for part in route.split("?", 1)[0].split("/")):
        raise ValueError("API route not permitted")
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "LYVRA-Bot-TODO-Metadata-Watch",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(
        "https://api.github.com" + route,
        data=None if payload is None else json.dumps(payload).encode("utf-8"),
        method="PATCH" if payload is not None else "GET",
        headers={**headers, **({"Content-Type": "application/json"} if payload is not None else {})},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def classify_path(path: str) -> set[str]:
    """Path heuristics nominate review; they do NOT decide native significance."""
    name = str(path).casefold()
    areas: set[str] = set()
    if name == "lyvra_native_runtime/current_pointer.json":
        areas.add("CURRENT_POINTER / native Release und Referenzen")
    if name.startswith("lyvra_native_runtime/"):
        areas.add("Native Runtime / Identität / Kontinuität / Sicherheit")
    if any(word in name for word in ("discord", "livecircle", "character", "facette",
                                     "relation", "garden", "bridge", "daemon")):
        areas.add("Discord-Facetten / Beziehungen / LiveCircle")
    if any(word in name for word in ("track", "music", "suno", "studio", "speech", "lyric")):
        areas.add("Music / Track Design / Speech")
    if any(word in name for word in ("privacy", "permission", "security", "auth", "api")):
        areas.add("Datenschutz / Berechtigungen / API")
    return areas


def candidate_from_compare(compare: dict) -> tuple[list[str], bool]:
    files = compare.get("files") or []
    areas: set[str] = set()
    for record in files:
        areas |= classify_path(record.get("filename", ""))
    incomplete = (len(files) >= 300 or compare.get("ahead_by", 0) > 250)
    if incomplete:
        areas.add("Großer Änderungsumfang: manueller vollständiger Diff erforderlich")
    return sorted(areas), incomplete


def update_issue_body(body: str, *, before: str, after: str,
                      areas: list[str], incomplete: bool = False) -> str:
    """Preserve all existing checkboxes and user edits; append only a delta candidate."""
    if not SHA_RE.fullmatch(before) or not SHA_RE.fullmatch(after):
        raise ValueError("Invalid source revision")
    match = MARKER_RE.search(body)
    if match is None or match.group(1) != before:
        raise ValueError("Tracker checkpoint changed; refuse lost update")
    if after == before:
        return body
    marker = f"<!-- LYVRA_NATIVE_HEAD:{after} -->"
    # GitHub compare lists public commit metadata; it is NOT a native full read.
    if areas:
        label = ", ".join(areas)
        description = (" (Diff unvollständig; manuelle Prüfung erforderlich)"
                       if incomplete else "")
        entry = (f"\n- [ ] **Native Änderung zur Bot-Relevanz prüfen**"
                 f" — [`{after[:12]}`](https://github.com/{NATIVE}/commit/{after})"
                 f" (seit `{before[:12]}`): {label}{description}. "
                 "Vor Integration: aktuellen Pointer und relevante Referenzen vollständig "
                 "lesen, Supersession beachten, technische Bot-Arbeit separat prüfen.\n")
        anchor = "## Arbeitsregeln"
        if anchor not in body:
            raise ValueError("Missing task section delimiter")
        body = body.replace(anchor, entry + "\n" + anchor, 1)
    body = MARKER_RE.sub(marker, body, count=1)
    if len(body) > 55000:
        raise ValueError("TODO issue too large; manual archival needed")
    return body


def run() -> str:
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        raise RuntimeError("GH_TOKEN missing; no write attempted")
    base = "/repos/" + NATIVE
    issue_path = f"/repos/{BOT}/issues/{ISSUE}"
    issue = api(issue_path, token=token)
    if issue.get("state") != "open":
        raise RuntimeError("Tracker issue closed; no auto-reopen")
    body = issue.get("body") or ""
    marker = MARKER_RE.search(body)
    if marker is None:
        raise RuntimeError("Missing durable checkpoint")
    before = marker.group(1)
    branch = api(base + "/branches/" + NATIVE_BRANCH, token=token)
    after = branch.get("commit", {}).get("sha", "")
    if not SHA_RE.fullmatch(after):
        raise RuntimeError("Invalid native productive HEAD")
    if after == before:
        return "NO_CHANGE: native productive HEAD unchanged"

    compare_path = (base + "/compare/" + urllib.parse.quote(before) + "..."
                    + urllib.parse.quote(after))
    try:
        compare = api(compare_path, token=token)
        if compare.get("status") not in ("ahead", "identical"):
            areas = ["Nicht-lineare Historie / Supersession manuell prüfen"]
            incomplete = True
        else:
            areas, incomplete = candidate_from_compare(compare)
    except urllib.error.HTTPError as exc:
        if exc.code not in (404, 409, 422):
            raise
        areas = ["Quell-Diff nicht verfügbar: aktuellen Zustand manuell auditieren"]
        incomplete = True

    new_body = update_issue_body(body, before=before, after=after,
                                 areas=areas, incomplete=incomplete)
    if new_body != body:
        api(issue_path, token=token, payload={"body": new_body})
    return (f"TODO_REVIEW_QUEUED: {after[:12]} / "
            f"{len(areas)} topic(s), incomplete={incomplete}")


if __name__ == "__main__":
    print(run())
