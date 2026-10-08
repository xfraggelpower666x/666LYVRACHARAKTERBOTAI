"""Offline regression checks: blob-readback is not behavioral approval."""
import unittest
from native_bridge.carrier_contract_coverage import summarize_contract_coverage

A="a"*40
B="b"*40
BLOB="c"*40

class CoverageTests(unittest.TestCase):
    def test_verified_blob_is_not_a_pass(self):
        result=summarize_contract_coverage(
            {"native_head":A,"results":{"pet":{"status":"CONTRACTS_READ",
             "evidence":[{"path":"LYVRA_PET/PET.md","blob_sha":BLOB}]}}},A,B)
        self.assertEqual(result["surfaces"]["pet"]["status"],"BLOB_READBACK_VERIFIED")
        self.assertFalse(result["surfaces"]["pet"]["compatibility_confirmed"])
        self.assertFalse(result["deployment_allowed"])
        self.assertEqual(result["compatibility"],"PARTIAL/INTEGRATION_GATES_OPEN")
    def test_stale_native_revision_rejected(self):
        with self.assertRaises(ValueError):
            summarize_contract_coverage({"native_head":"d"*40,"results":{}},A,B)
    def test_empty_evidence_remains_pending(self):
        result=summarize_contract_coverage({"native_head":A,"results":{}},A,B)
        self.assertTrue(all(x["status"]=="READBACK_PENDING" for x in result["surfaces"].values()))

if __name__=="__main__":
    unittest.main()
