import unittest
from native_bridge.carrier_release_gate import decision
from native_bridge.carrier_compatibility import SURFACES

A="a"*40
B="b"*40

class GateChecks(unittest.TestCase):
    def test_review_only(self):
        coverage={"native_head":A,"carrier_head":B,"surfaces":{s:{"status":"BLOB_READBACK_VERIFIED"} for s in SURFACES}}
        compatibility={"native_head":A,"carrier_head":B,"findings":[{"surface":s,"status":"COMPATIBLE_DEV"} for s in SURFACES]}
        result=decision(coverage,compatibility,native_head=A,carrier_head=B)
        self.assertFalse(result["deployment_authorized"])
        self.assertTrue(result["manual_approval_required"])
        self.assertTrue(all(v["release_gate"]=="REVIEW_ONLY" for v in result["surfaces"].values()))
    def test_stale_revision(self):
        with self.assertRaises(ValueError):
            decision({}, {}, native_head="invalid",carrier_head=B)

if __name__=="__main__":
    unittest.main()
