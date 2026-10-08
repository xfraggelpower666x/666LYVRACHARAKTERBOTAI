import json
import tempfile
import unittest
from pathlib import Path
from native_bridge.carrier_journal import SCHEMA, record_digest, append_local_journal
from native_bridge.carrier_journal_audit import verify_history, readback

def record():
    return {"schema": SCHEMA, "native_head": "a"*40,
            "native_mutated": False, "production_promoted": False,
            "identity_authority": "NATIVE_LYVRA_ONLY"}

def document(data):
    return {"schema": SCHEMA, "history": [{"record": data, "digest": record_digest(data)}]}

class JournalAuditTests(unittest.TestCase):
    def test_valid_history_readback(self):
        source = document(record())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"history.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            result = readback(path)
            self.assertEqual(result["integrity"], "PASS")
            self.assertEqual(result["entries"], 1)
    def test_tampering_rejected(self):
        source = document(record())
        source["history"][0]["record"]["native_head"] = "b"*40
        with self.assertRaises(ValueError):
            verify_history(source)
    def test_identity_drift_rejected(self):
        source = record()
        source["identity_authority"] = "SECOND_PERSONALITY"
        with self.assertRaises(ValueError):
            verify_history(document(source))
    def test_duplicate_rejected(self):
        source = document(record())
        source["history"].append(dict(source["history"][0]))
        with self.assertRaises(ValueError):
            verify_history(source)
    def test_corrupted_history_blocks_append(self):
        previous = document(record())
        previous["history"][0]["record"]["native_head"] = "b"*40
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"history.json"
            before = json.dumps(previous)
            path.write_text(before, encoding="utf-8")
            with self.assertRaises(ValueError):
                append_local_journal(path, record())
            self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_wrong_schema_rejected(self):
        with self.assertRaises(ValueError):
            verify_history({"schema": "UNKNOWN", "history": []})

if __name__ == "__main__":
    unittest.main()
