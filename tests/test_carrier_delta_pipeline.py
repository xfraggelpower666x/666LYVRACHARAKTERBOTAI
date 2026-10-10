import unittest
from native_bridge.carrier_delta_pipeline import preview

A="a"*40
B="b"*40
C="c"*40
def pointer(pet):
    return {"status":"CURRENT_PRODUCTIVE_VERIFIED",
            "current_known_whole_state":{"lyvra_pet":pet}}

class DeltaPipelineTests(unittest.TestCase):
    def test_changed_pet_enters_review_not_deployment(self):
        report=preview(pointer("old"),pointer("new"),A,B,C)
        self.assertIn("pet",[x["surface"] for x in report["delta"]["changes"]])
        self.assertFalse(report["auto_apply"])
        self.assertFalse(report["deployed"])
        self.assertEqual(report["analysis"]["compatibility"]["overall"],
                         "PARTIAL/INTEGRATION_GATES_OPEN")
    def test_same_value_no_delta(self):
        report=preview(pointer("same"),pointer("same"),A,B,C)
        self.assertEqual(report["delta"]["changes"],[])
        self.assertFalse(report["persisted"])
    def test_invalid_current_fails(self):
        with self.assertRaises(ValueError):
            preview(pointer("before"),{"status":"DRAFT","current_known_whole_state":{}},A,B,C)

if __name__=="__main__":
    unittest.main()
