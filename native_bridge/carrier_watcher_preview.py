"""DEV-only adapter for the existing path-delta watcher.

No scheduler changes, issue writes, bot runtime startup or native writes.
Path-derived changes are review hints; never compatibility evidence.
"""
from __future__ import annotations
from native_bridge.carrier_pipeline import analyze

HINTS = {
    "native_identity": ("identity/", "personality/", "character"),
    "personality_livecircle": ("livecircle", "personality/", "relations/", "memory"),
    "music_speech": ("music/", "track", "speech", "lyric", "studio2"),
    "website": ("weblyvra", "website/"),
    "dashboard": ("dashboard",),
    "visual_intelligence": ("visual", "sprite", "renderer"),
    "plugin_native": ("plugin/native", "native_plugin"),
    "plugin_account": ("plugin/account", "account_plugin"),
    "pet": ("lyvra_pet/", "pet/"),
}

def changed_surface_hints(paths):
    """Return sorted candidate areas, with no declaration of real causality."""
    result = set()
    for path in paths:
        name = str(path).lower().replace("\\", "/")
        for surface, patterns in HINTS.items():
            if any(pattern in name for pattern in patterns):
                result.add(surface)
    return tuple(sorted(result))


def preview_delta(native_head, bot_head, pointer, paths, classifier):
    """Pure integration preview for a watcher-produced diff."""
    paths = tuple(paths)
    report = analyze(native_head, bot_head, pointer,
                     changed_surfaces=changed_surface_hints(paths),
                     changed_paths=paths, classifier=classifier)
    return {
        "schema": "LYVRA_CARRIER_WATCHER_PREVIEW_v1",
        "origin": "EXISTING_DELTA_WATCHER_HINTS",
        "result": report,
        "issue_updated": False,
        "scheduler_updated": False,
        "native_updated": False,
        "deployed": False,
    }
