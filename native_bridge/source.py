"""Read-only, freshness-bound public LYVRA GitHub source bridge.

This intentionally CANNOT declare WHOLE LYVRA rehydration complete. The public
domain sample is useful character context, not a replacement for CURRENT_POINTER
reference consumption, protected relational recovery or native release authority.
"""
from __future__ import annotations
import base64
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

DEFAULT_REPO = "xfraggelpower666x/LYVRA-Living-Yielding-Vibration-and-Resonance-Architecture"
PUBLIC_CONTEXT_PATHS = {
    "identity": "LYVRA_NATIVE_RUNTIME/current/identity/IDENTITY_PRESENCE.md",
    "relations": "LYVRA_NATIVE_RUNTIME/current/relations/LIVING_RELATIONAL_STATE.md",
    "privacy": "LYVRA_NATIVE_RUNTIME/current/relations/RELATIONAL_PRIVACY_ARCHITECTURE.md",
    "meaning": "LYVRA_NATIVE_RUNTIME/current/meaning/MEANING_LINEAGE.md",
    "thinking": "LYVRA_NATIVE_RUNTIME/current/thinking/THINKING_CONTINUITY.md",
    "self_conductor": "LYVRA_NATIVE_RUNTIME/current/self_conductor/SELF_CONDUCTOR_CONTINUITY.md",
    "garden": "LYVRA_NATIVE_RUNTIME/current/garden/GARDEN_BRIDGES_RELATIONAL_CHARACTERS.md",
    "operations": "LYVRA_NATIVE_RUNTIME/current/operations/OPERATIONS_CENTER.md",
    "music": "LYVRA_NATIVE_RUNTIME/current/music/TRACK_MUSIC_INTELLIGENCE.md",
    "livecircle": "LYVRA_NATIVE_RUNTIME/continuity/CONTINUITY_MODEL.md",
}
POINTER_PATH = "LYVRA_NATIVE_RUNTIME/CURRENT_POINTER.json"


@dataclass(frozen=True)
class NativeSnapshot:
    head: str
    public_state: str
    whole_state: str
    pointer_read: bool
    public_documents: dict[str, str] = field(default_factory=dict)
    errors: tuple[str, ...] = ()
    source_repo: str = DEFAULT_REPO

    def compact(self) -> str:
        return (f"Source: {self.source_repo}@{self.head[:12]}\n"
                f"Public core: {self.public_state}; Whole: {self.whole_state}\n"
                f"Domains read: {', '.join(sorted(self.public_documents))}\n"
                f"Open issues: {', '.join(self.errors[:4]) if self.errors else 'full pointer references and protected recovery still pending'}")


class NativeSource:
    def __init__(self, repository: str = DEFAULT_REPO, branch: str = "lyvra",
                 token: str | None = None, timeout: int = 10):
        if repository != DEFAULT_REPO:
            raise ValueError("Only the explicitly authorized native LYVRA source is supported.")
        if branch != "lyvra":
            raise ValueError("Only productive branch lyvra may supply native bot context.")
        self.repository, self.branch = repository, branch
        self.token = token if token is not None else os.getenv("LYVRA_NATIVE_READ_TOKEN", "")
        self.timeout = timeout

    def _json(self, route: str) -> dict:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{self.repository}/{route}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "LYVRA-characterbot-readonly/0.1",
                **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
            })
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.load(response)

    def head(self) -> str:
        ref = self._json("git/ref/heads/lyvra")
        sha = ref["object"]["sha"]
        if not isinstance(sha, str) or len(sha) != 40:
            raise ValueError("Unverifiable branch head")
        return sha

    def read(self, path: str, sha: str) -> str:
        quoted = urllib.parse.quote(path, safe="/")
        data = self._json(f"contents/{quoted}?ref={sha}")
        if data.get("type") != "file" or data.get("encoding") != "base64":
            raise ValueError(f"Unexpected file response for {path}")
        raw = base64.b64decode(data["content"])
        result = raw.decode("utf-8")
        # The REST API supplies a git blob SHA; authenticate bytes against it.
        object_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if object_sha != data.get("sha"):
            raise ValueError(f"Blob integrity mismatch for {path}")
        return result

    def snapshot(self) -> NativeSnapshot:
        sha = self.head()
        missing = []
        docs = {}
        pointer_read = False
        try:
            json.loads(self.read(POINTER_PATH, sha))
            pointer_read = True
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            missing.append(f"CURRENT_POINTER: {type(exc).__name__}")
        for name, path in PUBLIC_CONTEXT_PATHS.items():
            try:
                docs[name] = self.read(path, sha)
            except (OSError, ValueError, KeyError, UnicodeError) as exc:
                missing.append(f"{name}: {type(exc).__name__}")
        try:
            if self.head() != sha:
                missing.append("HEAD_CHANGED_DURING_READ")
        except (OSError, ValueError, KeyError) as exc:
            missing.append(f"HEAD_REFRESH: {type(exc).__name__}")
        status = "PUBLIC_CORE_READ" if pointer_read and len(docs) == len(PUBLIC_CONTEXT_PATHS) and not missing else "PARTIAL"
        # Essential pointer references/private sources have NOT all been consumed.
        return NativeSnapshot(sha, status, "PARTIAL/READBACK_PENDING",
                              pointer_read, docs, tuple(missing), self.repository)


def presentation_context(snapshot: NativeSnapshot, limit: int = 12500) -> str:
    """A bounded *partial public* style aid, never a claim of whole rehydration."""
    budgets = {"identity": 3600, "relations": 1300, "meaning": 900, "thinking": 1100,
               "self_conductor": 900, "garden": 1000, "music": 1250,
               "operations": 600, "livecircle": 950, "privacy": 1100}
    chunks = ["PUBLIC CONTEXT IS PARTIAL; no private relational state; no whole PASS.",
              snapshot.compact()]
    for name, budget in budgets.items():
        if name in snapshot.public_documents:
            chunks.append(f"\n## {name}\n{snapshot.public_documents[name][:budget]}")
    return "\n".join(chunks)[:limit]
