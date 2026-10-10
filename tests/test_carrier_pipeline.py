"""Offline smoke checks for DEV-only carrier pipeline."""
import unittest
from native_bridge.carrier_pipeline import analyze

A = "a" * 40
B = "b" * 40
POINTER = {"status": "CURRENT_PRODUCTIVE_VERIFIED",
           "current_known_whole_state": {"lyvra_pet": "CURRENT_PRODUCTIVE"}}

class PipelineTests(unittest.TestCase):
    def test_fail_closed_without_attestations(self):
        result = analyze(A, B, POINTER, changed_surfaces=("pet",))
        self.assertEqual(result["compatibility"]["overall"], "PARTIAL/INTEGRATION_GATES_OPEN")
        self.assertEqual(result["impact"]["causality"], "HYPOTHESIS_NOT_PROVEN")
        self.assertFalse(result["approved_for_deployment"])
        self.assertFalse(result["persisted"])

    def test_unknown_surface_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze(A, B, POINTER, changed_surfaces=("foreign_system",))

    def test_watcher_topics_are_only_hints(self):
        result = analyze(A, B, POINTER, changed_paths=("music/a.md",),
                         classifier=lambda path: {"Music"} if "music" in path else set())
        self.assertEqual(result["journal_candidate"]["topics"], ["Music"])
        self.assertFalse(result["native_modified"])

if __name__ == "__main__":
    unittest.main()
