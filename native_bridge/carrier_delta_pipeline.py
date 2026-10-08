"""Pure DEV preview combining pointer delta with carrier analysis.

No scheduler, GitHub issue, persistent file, native or bot production writes.
"""
from native_bridge.carrier_pointer_delta import compare_pointers
from native_bridge.carrier_pipeline import analyze

def preview(previous, current, old_head, new_head, carrier_head, *,
            changed_paths=(), classifier=lambda path: set()):
    delta = compare_pointers(previous, current, old_head, new_head)
    affected = tuple(sorted({item["surface"] for item in delta["changes"]}))
    analysis = analyze(new_head, carrier_head, current,
                       changed_surfaces=affected,
                       changed_paths=changed_paths, classifier=classifier)
    return {"schema":"LYVRA_CARRIER_DELTA_PIPELINE_v1",
            "delta":delta,"analysis":analysis,
            "source":"PUBLIC_POINTER_METADATA",
            "auto_apply":False,"persisted":False,"deployed":False}
