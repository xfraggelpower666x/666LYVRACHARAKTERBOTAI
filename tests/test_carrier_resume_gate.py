import unittest
from native_bridge.carrier_resume_gate import resume_gate

A="a"*40
B="b"*40
def item():
    return {"native_head":A,"carrier_head":B,"native_mutated":False,"production_promoted":False}

class ResumeTests(unittest.TestCase):
    def test_fresh_is_only_candidate(self):
        r=resume_gate(item(),A,B)
        self.assertEqual(r["status"],"REVIEW_CANDIDATE")
        self.assertFalse(r["deployment_authorized"])
        self.assertFalse(r["restored"])
    def test_native_drift_requires_refresh(self):
        self.assertEqual(resume_gate(item(),"c"*40,B)["status"],"REFRESH_REQUIRED")
    def test_carrier_drift_requires_refresh(self):
        self.assertEqual(resume_gate(item(),A,"c"*40)["status"],"REFRESH_REQUIRED")
    def test_mutation_marker_fails(self):
        x=item()
        x["native_mutated"]=True
        with self.assertRaises(ValueError):
            resume_gate(x,A,B)
if __name__=="__main__":
    unittest.main()
