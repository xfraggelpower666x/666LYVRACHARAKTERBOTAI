"""Offline safety tests for pinned native contract reader."""
import hashlib
import unittest
from native_bridge.carrier_contracts import collect

HEAD="a"*40
BODY="safe public contract"
RAW=BODY.encode()
BLOB=hashlib.sha1(b"blob "+str(len(RAW)).encode()+b"\0"+RAW).hexdigest()

class Source:
    def read(self,path,head):
        assert head==HEAD
        return BODY

class ContractTests(unittest.TestCase):
    def test_matching_blob_is_evidence_not_compatibility(self):
        out=collect(Source(),HEAD,{"pet":[{"path":"LYVRA_PET/manifest.md","blob_sha":BLOB}]})
        self.assertEqual(out["results"]["pet"]["status"],"CONTRACTS_READ")
        self.assertFalse(out["results"]["pet"]["compatible"])
    def test_wrong_blob_is_blocked(self):
        out=collect(Source(),HEAD,{"pet":[{"path":"LYVRA_PET/manifest.md","blob_sha":"b"*40}]})
        self.assertIn("BLOB_MISMATCH",out["results"]["pet"]["blockers"])
    def test_private_or_traversal_path_rejected(self):
        out=collect(Source(),HEAD,{"pet":[{"path":"../secrets","blob_sha":BLOB}]})
        self.assertIn("INVALID_CONTRACT_REFERENCE",out["results"]["pet"]["blockers"])
    def test_missing_contract_is_pending(self):
        out=collect(Source(),HEAD,{})
        self.assertTrue(all(x["status"]=="READBACK_PENDING" for x in out["results"].values()))
if __name__=="__main__":
    unittest.main()
