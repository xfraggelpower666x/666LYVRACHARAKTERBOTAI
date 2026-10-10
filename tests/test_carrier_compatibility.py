"""Offline regression checks for the passive carrier compatibility auditor."""
import unittest

from native_bridge.carrier_compatibility import audit, SURFACES, REQUIRED

NATIVE_SHA = "a" * 40
BOT_SHA = "b" * 40


def evidence():
    native = {"head": NATIVE_SHA, "surfaces": {}}
    bot = {"head": BOT_SHA, "surfaces": {}}
    for name in SURFACES:
        data = {key: "verified-reference" for key in REQUIRED[name]}
        data.update(fingerprint="hash-" + name, evidence=["git:" + NATIVE_SHA])
        native["surfaces"][name] = data
        bot["surfaces"][name] = {
            "native_fingerprint": "hash-" + name, "tested": True, "readback": True
        }
    return native, bot


class CarrierCompatibilityTests(unittest.TestCase):
    def test_missing_proof_fails_closed(self):
        native, bot = evidence()
        del native["surfaces"]["pet"]["pet_asset_provenance"]
        result = audit(native, bot)
        pet = next(x for x in result["findings"] if x["surface"] == "pet")
        self.assertEqual(pet["status"], "READBACK_PENDING")
        self.assertEqual(result["overall"], "PARTIAL/INTEGRATION_GATES_OPEN")

    def test_contract_drift_needs_adapter_review(self):
        native, bot = evidence()
        native["surfaces"]["personality_livecircle"]["fingerprint"] = "updated"
        report = audit(native, bot)
        self.assertEqual(report["findings"][1]["status"], "ADAPTATION_REVIEW")

    def test_missing_test_never_passes(self):
        native, bot = evidence()
        bot["surfaces"]["website"]["tested"] = False
        report = audit(native, bot)
        self.assertEqual(report["findings"][3]["status"], "TEST_PENDING")

    def test_dev_pass_is_not_deployment(self):
        native, bot = evidence()
        result = audit(native, bot)
        self.assertEqual(result["overall"], "DEV_REVIEW_ONLY")
        self.assertFalse(result["whole_rehydration_claim"])
        self.assertFalse(result["native_identity_mutation"])
        self.assertFalse(result["bot_production_mutation"])

    def test_bad_revision_rejected(self):
        native, bot = evidence()
        native["head"] = "latest"
        with self.assertRaises(ValueError):
            audit(native, bot)


if __name__ == "__main__":
    unittest.main()
