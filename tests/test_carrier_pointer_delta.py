import unittest
from native_bridge.carrier_pointer_delta import compare_pointers
A="a"*40
B="b"*40
def pointer(value):
    return {"status":"CURRENT_PRODUCTIVE_VERIFIED",
            "current_known_whole_state":{"lyvra_pet":value}}
class PointerDeltaTests(unittest.TestCase):
    def test_changed_pet_is_candidate_only(self):
        result=compare_pointers(pointer("OLD"),pointer("NEW"),A,B)
        self.assertIn("pet",[x["surface"] for x in result["changes"]])
        self.assertFalse(result["promotion_authorized"])
        self.assertTrue(all(not x["integration_verified"] for x in result["changes"]))
    def test_same_pointer_is_no_change(self):
        self.assertEqual(compare_pointers(pointer("SAME"),pointer("SAME"),A,B)["changes"],[])
    def test_unverified_current_rejected(self):
        with self.assertRaises(ValueError):
            compare_pointers(pointer("X"),{"status":"DRAFT","current_known_whole_state":{}},A,B)
if __name__=="__main__":
    unittest.main()
