"""Offline checks for watcher preview safety."""
import unittest
from native_bridge.carrier_watcher_preview import changed_surface_hints, preview_delta

A = "a"*40
B = "b"*40
POINTER = {"status":"CURRENT_PRODUCTIVE_VERIFIED",
           "current_known_whole_state":{"lyvra_pet":"CURRENT_PRODUCTIVE"}}

class WatcherPreviewTests(unittest.TestCase):
    def test_pet_and_speech_are_candidates(self):
        hints = changed_surface_hints(["LYVRA_PET/app/icon.png", "speech/voice.md"])
        self.assertIn("pet", hints)
        self.assertIn("music_speech", hints)

    def test_preview_never_writes_or_claims_production(self):
        result = preview_delta(A, B, POINTER, ["LYVRA_PET/app/icon.png"],
                               lambda path: {"PET candidate"})
        self.assertFalse(result["issue_updated"])
        self.assertFalse(result["deployed"])
        self.assertFalse(result["scheduler_updated"])
        self.assertEqual(result["result"]["compatibility"]["overall"],
                         "PARTIAL/INTEGRATION_GATES_OPEN")
        self.assertFalse(result["result"]["approved_for_deployment"])

    def test_unknown_path_does_not_invent_facet(self):
        self.assertEqual(changed_surface_hints(["docs/README.md"]), ())
if __name__ == "__main__":
    unittest.main()
