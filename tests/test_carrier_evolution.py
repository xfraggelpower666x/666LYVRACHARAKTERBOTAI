"""No-network tests for read-only Native pointer candidate extraction."""
import unittest
from native_bridge.carrier_evolution import candidates_from_pointer, scan, compatibility_from_candidates

SHA = "a" * 40

class FakeNative:
    def __init__(self, sha=SHA, second=None):
        self.sha, self.second, self.n = sha, second, 0
    def head(self):
        self.n += 1
        return self.second if self.n > 1 and self.second else self.sha
    def read(self, path, ref):
        assert ref == self.sha
        return '{"status":"CURRENT_PRODUCTIVE_VERIFIED","current_known_whole_state":{"lyvra_pet":"CURRENT_PRODUCTIVE"}}'

class CarrierEvolutionTests(unittest.TestCase):
    def test_pointer_is_not_integration_proof(self):
        r = candidates_from_pointer({"status":"CURRENT_PRODUCTIVE_VERIFIED",
             "current_known_whole_state":{"lyvra_pet":"CURRENT_PRODUCTIVE"}}, SHA)
        self.assertEqual(len(r["surfaces"]), 9)
        self.assertFalse(next(x for x in r["surfaces"] if x["surface"] == "pet")["integration_verified"])
        self.assertEqual(compatibility_from_candidates(r, "b"*40)["overall"],
                         "PARTIAL/INTEGRATION_GATES_OPEN")

    def test_source_pinned_to_one_head(self):
        r = scan(FakeNative())
        self.assertEqual(r["native_head"], SHA)
        self.assertEqual(r["source"], "CURRENT_POINTER_METADATA_ONLY")

    def test_changed_head_rejected(self):
        with self.assertRaises(RuntimeError):
            scan(FakeNative(second="c"*40))

    def test_unverified_pointer_rejected(self):
        with self.assertRaises(ValueError):
            candidates_from_pointer({"status":"DRAFT","current_known_whole_state":{}}, SHA)

    def test_actual_native_website_field_is_detected(self):
        sample = {"status": "CURRENT_PRODUCTIVE_VERIFIED",
                  "current_known_whole_state": {"lyvra_pet_website_deployment": "VERIFIED"}}
        result = candidates_from_pointer(sample, SHA)
        website = next(x for x in result["surfaces"] if x["surface"] == "website")
        self.assertEqual(website["status"], "REVIEW_CANDIDATE")
        self.assertFalse(website["integration_verified"])

    def test_invalid_pinned_head_rejected(self):
        with self.assertRaises(ValueError):
            candidates_from_pointer({"status": "CURRENT_PRODUCTIVE_VERIFIED",
                                     "current_known_whole_state": {}}, "latest")

    def test_missing_surface_is_open(self):
        r = candidates_from_pointer({"status":"CURRENT_PRODUCTIVE_VERIFIED",
                                     "current_known_whole_state":{}}, SHA)
        self.assertTrue(all(x["status"]=="READBACK_PENDING" for x in r["surfaces"]))

if __name__ == "__main__":
    unittest.main()
