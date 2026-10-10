"""Native->Bot read-only bridge tests. No external network."""
import base64
import hashlib
import json
import unittest
from unittest.mock import patch

from native_bridge import repo_handoff_probe as probe


def payload():
    return {
        "schema": probe.SCHEMA,
        "event_id": "LYVRA-CODEFORGE-BOT-EVOLUTION-2026-10-10-001",
        "source": {"repository": probe.NATIVE, "branch": "lyvra", "head": "b"*40},
        "destination": {"repository": "xfraggelpower666x/666LYVRACHARAKTERBOTAI"},
        "proposals": [{"id": "BOT-001", "reason": "Better communication"}],
    }


class NativeRepoProbeTests(unittest.TestCase):
    def test_candidate_is_not_adoption(self):
        r = probe.check_handoff(payload(), retrieved_head="a"*40, content_sha="c"*40)
        self.assertEqual(r["status"], "READ_ONLY_RECEIVED_CANDIDATE")
        self.assertFalse(r["adopted_by_bot"])
        self.assertFalse(r["acknowledged_to_native"])
        self.assertFalse(r["whole_lyvra_rehydrated"])

    def test_wrong_repository_rejected(self):
        x = payload()
        x["source"]["repository"] = "stranger"
        with self.assertRaises(ValueError):
            probe.check_handoff(x, retrieved_head="a"*40, content_sha="c"*40)

    def test_duplicate_proposals_rejected(self):
        x = payload()
        x["proposals"].append(x["proposals"][0])
        with self.assertRaises(ValueError):
            probe.check_handoff(x, retrieved_head="a"*40, content_sha="c"*40)

    def test_pinned_read_and_blob_integrity(self):
        raw = json.dumps(payload()).encode()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        responses = iter([
            {"commit": {"sha": "a"*40}},
            {"encoding": "base64", "content": base64.b64encode(raw).decode(), "sha": sha},
            {"commit": {"sha": "a"*40}},
        ])
        with patch.object(probe, "_github_json", side_effect=lambda *a, **k: next(responses)):
            r = probe.read_native_handoff()
        self.assertEqual(r["handoff_git_blob"], sha)

    def test_hash_tampering_rejected(self):
        raw = json.dumps(payload()).encode()
        responses = iter([
            {"commit": {"sha": "a"*40}},
            {"encoding": "base64", "content": base64.b64encode(raw).decode(), "sha": "0"*40},
        ])
        with patch.object(probe, "_github_json", side_effect=lambda *a, **k: next(responses)):
            with self.assertRaises(ValueError):
                probe.read_native_handoff()

    def test_head_drift_quarantined(self):
        raw = json.dumps(payload()).encode()
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        responses = iter([
            {"commit": {"sha": "a"*40}},
            {"encoding": "base64", "content": base64.b64encode(raw).decode(), "sha": sha},
            {"commit": {"sha": "b"*40}},
        ])
        with patch.object(probe, "_github_json", side_effect=lambda *a, **k: next(responses)):
            with self.assertRaisesRegex(ValueError, "moved"):
                probe.read_native_handoff()


if __name__ == "__main__":
    unittest.main()
