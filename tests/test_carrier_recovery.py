import unittest
from native_bridge.carrier_recovery import recovery_plan
from native_bridge.carrier_journal import SCHEMA, record_digest

A="a"*40
B="b"*40

def history():
    r={"schema":SCHEMA,"native_head":A,"native_mutated":False,
       "production_promoted":False,"identity_authority":"NATIVE_LYVRA_ONLY"}
    return {"schema":SCHEMA,"history":[{"record":r,"digest":record_digest(r)}]}

class RecoveryTests(unittest.TestCase):
    def test_valid_candidate_never_auto_restores(self):
        out=recovery_plan(history(),A)
        self.assertEqual(out["status"],"RECOVERY_CANDIDATE_VERIFIED")
        self.assertFalse(out["restored"])
        self.assertFalse(out["deployment_authorized"])
    def test_newer_native_requires_revalidation(self):
        out=recovery_plan(history(),B)
        self.assertEqual(out["status"],"STALE_REFERENCE_REVALIDATE")
        self.assertFalse(out["restored"])
    def test_modified_journal_fails(self):
        h=history()
        h["history"][0]["record"]["native_head"]=B
        with self.assertRaises(ValueError):
            recovery_plan(h,A)
if __name__=="__main__":
    unittest.main()
