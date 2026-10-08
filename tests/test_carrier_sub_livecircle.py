import tempfile
import unittest
from pathlib import Path
from native_bridge.carrier_delta_pipeline import preview
from native_bridge.carrier_sub_livecircle import prepare_circle_record, persist_dev_report

A="a"*40
B="b"*40
C="c"*40
def pointer(v):
    return {"status":"CURRENT_PRODUCTIVE_VERIFIED",
            "current_known_whole_state":{"lyvra_pet":v}}

class CircleTests(unittest.TestCase):
    def test_identity_remains_native(self):
        report=preview(pointer("old"),pointer("new"),A,B,C)
        record=prepare_circle_record(report)
        self.assertEqual(record["identity_authority"],"NATIVE_LYVRA_ONLY")
        self.assertEqual(record["circle_state"],"REVIEW_PENDING")

    def test_explicit_local_persistence_idempotent(self):
        report=preview(pointer("old"),pointer("new"),A,B,C)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"carrier.json"
            self.assertTrue(persist_dev_report(path,report))
            self.assertFalse(persist_dev_report(path,report))

    def test_unsafe_report_is_rejected(self):
        report=preview(pointer("old"),pointer("new"),A,B,C)
        report["deployed"]=True
        with self.assertRaises(ValueError):
            prepare_circle_record(report)

if __name__=="__main__":
    unittest.main()
