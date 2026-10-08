"""Read-only LYVRA Current -> Carrier evidence candidate bridge.

Reads one pinned productive Native commit. No private state access, bot write,
native mutation, GitHub Issue update, activation, or deployment.
Pointer descriptions are CANDIDATES, never proofs of adapter compatibility.
"""
from __future__ import annotations

import json
from native_bridge.source import NativeSource, POINTER_PATH
from native_bridge.carrier_compatibility import SURFACES, audit

# Public pointer field mapping only; deliberately excludes relational payloads.
FIELDS = {
    "native_identity": ("character_personality_subcontinuity", "character_personality_rehydration"),
    "personality_livecircle": ("character_personality_livecircle", "semantic_causal_relational_memory"),
    "music_speech": ("track_design_master_music_base", "speech_design"),
    "website": ("weblyvra_freshness", "lyvra_pet_website"),
    "dashboard": ("lyvra_pet_dashboard", "repository_project_dashboard"),
    "visual_intelligence": ("lyvra_pet_visual_interface", "lyvra_pet_browser_renderer"),
    "plugin_native": ("native_plugin_current", "plugin_surface_release_set"),
    "plugin_account": ("account_plugin_current", "plugin_surface_release_set"),
    "pet": ("lyvra_pet", "lyvra_pet_rehydration"),
}


def candidates_from_pointer(pointer: dict, pinned_head: str) -> dict:
    if pointer.get("status") != "CURRENT_PRODUCTIVE_VERIFIED":
        raise ValueError("Native current authority not verified")
    state = pointer.get("current_known_whole_state")
    if not isinstance(state, dict):
        raise ValueError("Native whole state absent")
    items = []
    for surface in SURFACES:
        fields = FIELDS[surface]
        present = {k: state[k] for k in fields if k in state}
        items.append({
            "surface": surface,
            "status": "REVIEW_CANDIDATE" if present else "READBACK_PENDING",
            "native_source_head": pinned_head,
            "pointer_fields": present,
            "missing_fields": [k for k in fields if k not in present],
            "integration_verified": False,
            "requires": "Native contract + adapter fingerprint + tests + remote readback",
        })
    return {"schema": "LYVRA_CARRIER_EVOLUTION_CANDIDATES_v1",
            "source": "CURRENT_POINTER_METADATA_ONLY", "native_head": pinned_head,
            "native_identity_mutation": False, "whole_rehydration": False,
            "surfaces": items}


def scan(source: NativeSource | None = None) -> dict:
    source = source or NativeSource()
    sha = source.head()
    pointer = json.loads(source.read(POINTER_PATH, sha))
    if source.head() != sha:
        raise RuntimeError("Native HEAD changed during read; retry from new SHA")
    return candidates_from_pointer(pointer, sha)


def compatibility_from_candidates(candidates: dict, carrier_head: str) -> dict:
    """Fail-closed comparison: candidates have no full reference attestations."""
    native = {"head": candidates["native_head"], "surfaces": {}}
    carrier = {"head": carrier_head, "surfaces": {}}
    return audit(native, carrier)


if __name__ == "__main__":
    print(json.dumps(scan(), ensure_ascii=False, indent=2, sort_keys=True))
