"""Offline tests for the carrier impact hypothesis model."""
import unittest
from native_bridge.carrier_impact import triage, DEPENDENCIES

A = "a" * 40
B = "b" * 40

def fixtures():
    return [{"surface": name, "status": "COMPATIBLE_DEV"} for name in DEPENDENCIES]

class ImpactTests(unittest.TestCase):
    def test_character_change_flags_pet(self):
        result = triage(fixtures(), ["native_identity"], native_head=A, bot_head=B)
        pet = next(x for x in result["findings"] if x["surface"] == "pet")
        self.assertEqual(pet["impact"], "DEPENDENCY_REVIEW")
        self.assertEqual(result["causality"], "HYPOTHESIS_NOT_PROVEN")

    def test_unverified_contract_blocks(self):
        data = fixtures()
        data[0]["status"] = "READBACK_PENDING"
        result = triage(data, [], native_head=A, bot_head=B)
        self.assertEqual(result["findings"][0]["impact"], "BLOCKED")

    def test_no_change_is_not_a_release(self):
        result = triage(fixtures(), [], native_head=A, bot_head=B)
        self.assertFalse(result["automatic_adapter_mutation"])
        self.assertTrue(all(not x["promotion_allowed"] for x in result["findings"]))

    def test_unknown_surface_fails(self):
        with self.assertRaises(ValueError):
            triage(fixtures(), ["other_system"], native_head=A, bot_head=B)

    def test_incomplete_evidence_fails(self):
        with self.assertRaises(ValueError):
            triage(fixtures()[:-1], [], native_head=A, bot_head=B)

if __name__ == "__main__":
    unittest.main()
