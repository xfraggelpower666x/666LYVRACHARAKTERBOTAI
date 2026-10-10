"""No-network reciprocal handoff outbox tests."""
import json
import tempfile
import unittest
from pathlib import Path

from native_bridge.reciprocal_outbox import queue_review_candidate, review_receipt
from native_bridge.reciprocal_learning import prepare_candidate


def sample():
    return {
        "bot_head": "b"*40, "native_head_observed": "a"*40,
        "source_type": "CREATIVE_IDEA",
        "observation": "An offline synthetic idea for explaining psytrance rhythm",
        "causal_relevance": "Clear and kind music communication",
        "evidence_class": "SYNTHETIC_ONLY",
        "provenance": "Offline synthetic test, no Discord messages",
        "uncertainty": "Needs native assessment",
        "suggested_native_target": "music-knowledge-communication",
        "suggested_test": "Check evidence and content privacy",
        "privacy_class": "PUBLIC_SAFE"
    }


class OutboxTests(unittest.TestCase):
    def test_explicit_privacy_review_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                queue_review_candidate(tmp, sample())

    def test_exact_bytes_repeat_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = queue_review_candidate(tmp, sample(), privacy_reviewed=True)
            second = queue_review_candidate(tmp, sample(), privacy_reviewed=True)
            self.assertEqual(first["status"], "STORED_LOCAL_ONLY")
            self.assertEqual(second["status"], "ALREADY_STORED_IDENTICAL")
            self.assertFalse(first["network_sent"])
            envelope = json.loads(Path(first["location"]).read_text())
            self.assertEqual(envelope["event_id"], first["event_id"])
            self.assertFalse(envelope["native_adopted"])

    def test_conflicting_stored_file_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            event = prepare_candidate(sample())["event_id"]
            target = Path(tmp) / (event + ".json")
            target.write_text("historical record protected", encoding="utf-8")
            with self.assertRaises(ValueError):
                queue_review_candidate(tmp, sample(), privacy_reviewed=True)
            self.assertEqual(target.read_text(), "historical record protected")

    def test_reject_private_field_before_storage(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = sample()
            candidate["discord_user_id"] = "not-permitted"
            with self.assertRaises(ValueError):
                queue_review_candidate(tmp, candidate, privacy_reviewed=True)
            self.assertFalse(list(Path(tmp).iterdir()))

    def test_receipt_ack_not_adoption(self):
        candidate = prepare_candidate(sample())
        result = review_receipt(candidate, {"event_id":candidate["event_id"], "decision":"ACK"})
        self.assertFalse(result["native_adopted"])
        self.assertFalse(result["delivery_confirmed"])

    def test_adoption_claim_still_requires_independent_readback(self):
        candidate = prepare_candidate(sample())
        result = review_receipt(candidate, {"event_id":candidate["event_id"],
                                "decision":"ADOPTED", "native_adoption_commit":"c"*40,
                                "native_readback_pass":True})
        self.assertFalse(result["native_adopted"])
        self.assertEqual(result["status"], "ADOPTION_REPORTED_READBACK_PENDING")

    def test_reject_relative_outbox_path(self):
        with self.assertRaises(ValueError):
            queue_review_candidate("relative/path", sample(), privacy_reviewed=True)


if __name__ == "__main__":
    unittest.main()
