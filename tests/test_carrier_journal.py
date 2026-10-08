"""Offline tests for DEV-only carrier journal and passive watcher bridge."""
import json
import tempfile
import unittest
from pathlib import Path

from native_bridge.carrier_journal import (
    SCHEMA, append_local_journal, build_record, watcher_topics
)

A = "a" * 40
B = "b" * 40

def classifier(path):
    return {"Music"} if "music" in path else set()

def pointer():
    return {"status": "CURRENT_PRODUCTIVE_VERIFIED",
            "current_known_whole_state": {"lyvra_pet": "CURRENT_PRODUCTIVE"}}

class CarrierJournalTests(unittest.TestCase):
    def test_existing_watcher_classifier_is_reused_as_hint(self):
        self.assertEqual(watcher_topics(["music/track.md", "music/voice.md"], classifier),
                         ["Music"])

    def test_candidate_not_misreported_as_compatible(self):
        record = build_record(A, B, pointer(), ["music/track.md"], classifier)
        self.assertEqual(record["compatibility"], "PARTIAL/INTEGRATION_GATES_OPEN")
        self.assertFalse(record["whole_rehydration_claim"])
        self.assertEqual(len(record["surfaces"]), 9)

    def test_history_append_idempotent(self):
        record = build_record(A, B, pointer(), [], classifier)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "carrier.json"
            self.assertTrue(append_local_journal(path, record))
            self.assertFalse(append_local_journal(path, record))
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema"], SCHEMA)
            self.assertEqual(len(data["history"]), 1)

    def test_refuse_unknown_existing_schema(self):
        record = build_record(A, B, pointer(), [], classifier)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "carrier.json"
            path.write_text('{"schema":"other","history":[]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                append_local_journal(path, record)
            self.assertIn('"other"', path.read_text(encoding="utf-8"))

    def test_promotion_marker_forbidden(self):
        record = build_record(A, B, pointer(), [], classifier)
        record["production_promoted"] = True
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                append_local_journal(Path(tmp) / "carrier.json", record)

if __name__ == "__main__":
    unittest.main()
