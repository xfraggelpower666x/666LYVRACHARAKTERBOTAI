"""Offline safety/causal checks for LYVRA one-identity reciprocal handoff."""
import unittest

from native_bridge.reciprocal_learning import prepare_candidate, validate_receipt, SCHEMA

NATIVE_HEAD = "a" * 40
BOT_HEAD = "b" * 40


def sample():
    return {
        "bot_head": BOT_HEAD,
        "native_head_observed": NATIVE_HEAD,
        "source_type": "CREATIVE_IDEA",
        "observation": "Short musical explanations helped audiences understand rhythm",
        "causal_relevance": "Conversation quality, not Suno prompt generation",
        "evidence_class": "DEV_EXPERIMENT",
        "provenance": "Offline synthetic example, not a real Discord event",
        "uncertainty": "Unconfirmed until authorized real-world review",
        "suggested_native_target": "Music knowledge communication",
        "suggested_test": "Review answer clarity and privacy",
        "privacy_class": "PUBLIC_SAFE",
    }


class ReciprocalLearningTests(unittest.TestCase):
    def test_review_only_and_one_identity(self):
        r = prepare_candidate(sample())
        self.assertEqual(r["schema"], SCHEMA)
        self.assertEqual(r["direction"], "BOT_TO_NATIVE")
        self.assertEqual(r["identity_authority"], "WHOLE_LYVRA_ONLY")
        self.assertFalse(r["native_adopted"])
        self.assertFalse(r["discord_deployed"])

    def test_reproducible_event_id(self):
        self.assertEqual(prepare_candidate(sample())["event_id"],
                         prepare_candidate(sample())["event_id"])

    def test_reject_raw_private_data(self):
        for field in ("raw_message", "discord_user_id", "private_memory", "transcript"):
            with self.subTest(field=field):
                payload = sample()
                payload[field] = "sensitive"
                with self.assertRaises(ValueError):
                    prepare_candidate(payload)

    def test_reject_unclassified_or_private(self):
        for privacy in ("PRIVATE", "", "UNKNOWN"):
            with self.subTest(privacy=privacy):
                payload = sample()
                payload["privacy_class"] = privacy
                with self.assertRaises(ValueError):
                    prepare_candidate(payload)

    def test_reject_non_pinned_head(self):
        payload = sample()
        payload["native_head_observed"] = "latest"
        with self.assertRaises(ValueError):
            prepare_candidate(payload)

    def test_consent_required_for_aggregate(self):
        payload = sample()
        payload["privacy_class"] = "CONSENTED_REDACTED_AGGREGATE"
        with self.assertRaises(ValueError):
            prepare_candidate(payload)
        payload["consent_verified"] = True
        self.assertEqual(prepare_candidate(payload)["status"], "NATIVE_REVIEW_PENDING")

    def test_reject_invented_source_type(self):
        payload = sample()
        payload["source_type"] = "AUTONOMOUS_PERSONALITY_REWRITE"
        with self.assertRaises(ValueError):
            prepare_candidate(payload)

    def test_ack_ne_adoption(self):
        event_id = prepare_candidate(sample())["event_id"]
        result = validate_receipt({"event_id": event_id, "decision": "ACK"}, event_id)
        self.assertFalse(result["native_adopted"])
        self.assertEqual(result["status"], "BOT_RECEIPT_ONLY")

    def test_adoption_requires_native_readback(self):
        event_id = prepare_candidate(sample())["event_id"]
        with self.assertRaises(ValueError):
            validate_receipt({"event_id": event_id, "decision": "ADOPTED"}, event_id)
        report = {"event_id": event_id, "decision": "ADOPTED",
                  "native_adoption_commit": "c" * 40, "native_readback_pass": True}
        unverified = validate_receipt(report, event_id)
        self.assertFalse(unverified["native_adopted"])
        self.assertEqual(unverified["status"], "ADOPTION_REPORTED_READBACK_PENDING")
        with self.assertRaises(ValueError):
            validate_receipt(report, event_id, verified_native_readback={
                "source": "INDEPENDENT_NATIVE_GITHUB_READBACK",
                "commit": "d" * 40, "event_id": event_id, "matched": True
            })
        trusted_readback = {"source": "INDEPENDENT_NATIVE_GITHUB_READBACK",
                            "commit": "c" * 40, "event_id": event_id,
                            "matched": True}
        confirmed = validate_receipt(report, event_id, verified_native_readback=trusted_readback)
        self.assertTrue(confirmed["native_adopted"])
        self.assertFalse(confirmed["independent_readback_performed_here"])


if __name__ == "__main__":
    unittest.main()
