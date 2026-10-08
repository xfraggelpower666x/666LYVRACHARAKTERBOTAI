"""DEV-only orchestration: pointer candidates -> compatibility -> causal review.

Pure analysis; does not write native, Discord, GitHub issues or release pointers.
Changes are candidate hints, not proven causal facts. No automatic promotion.
"""
from __future__ import annotations

from native_bridge.carrier_evolution import candidates_from_pointer
from native_bridge.carrier_compatibility import audit, SURFACES
from native_bridge.carrier_impact import triage
from native_bridge.carrier_journal import build_record


def analyze(native_head, bot_head, pointer, *, changed_surfaces=(),
            changed_paths=(), classifier=lambda path: set(),
            native_attestations=None, carrier_attestations=None):
    candidates = candidates_from_pointer(pointer, native_head)
    # A metadata candidate MUST NOT become an attestation implicitly.
    native = {"head": native_head, "surfaces": native_attestations or {}}
    carrier = {"head": bot_head, "surfaces": carrier_attestations or {}}
    compatibility = audit(native, carrier)
    impact = triage(compatibility["findings"], changed_surfaces,
                    native_head=native_head, bot_head=bot_head)
    journal = build_record(native_head, bot_head, pointer, changed_paths, classifier)
    return {
        "schema": "LYVRA_CARRIER_DEV_ANALYSIS_v1",
        "candidates": candidates,
        "compatibility": compatibility,
        "impact": impact,
        "journal_candidate": journal,
        "persisted": False,
        "native_modified": False,
        "bot_production_modified": False,
        "approved_for_deployment": False,
    }
