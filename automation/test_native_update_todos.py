"""Offline tests: issue-only bot TODO watcher never modifies bot/native code."""
import unittest
import io
from unittest.mock import patch

from native_update_todos import (
    candidate_from_compare, classify_path, update_issue_body, api,
)

OLD = "1" * 40
NEW = "2" * 40
BODY = ("# Native bot TODO\n\n## Offene Integrationsaufgaben\n"
        "- [x] Historischer Test erledigt\n"
        "## Arbeitsregeln\nNoch keine Freigabe.\n\n"
        f"<!-- LYVRA_NATIVE_HEAD:{OLD} -->\n")


class ApiRouteGuardTests(unittest.TestCase):
    def test_compare_separator_is_not_path_traversal(self):
        route = "/repos/xfraggelpower666x/sample/compare/" + OLD + "..." + NEW
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b"{}")) as mocked:
            self.assertEqual(api(route), {})
        mocked.assert_called_once()

    def test_parent_path_segment_rejected(self):
        with self.assertRaises(ValueError):
            api("/repos/xfraggelpower666x/sample/../private")

    def test_missing_repo_prefix_rejected(self):
        with self.assertRaises(ValueError):
            api("/users/xfraggelpower666x")


class TodoClassificationTests(unittest.TestCase):
    def test_native_pointer_queues_review(self):
        self.assertIn("CURRENT_POINTER / native Release und Referenzen",
                      classify_path("LYVRA_NATIVE_RUNTIME/CURRENT_POINTER.json"))

    def test_discord_and_music_detected(self):
        categories = classify_path("LYVRA_NATIVE_RUNTIME/adapters/discord_character_bot/speech.py")
        self.assertTrue(any("Discord" in x for x in categories))
        self.assertTrue(any("Music" in x for x in categories))

    def test_web_only_does_not_force_bot_task(self):
        self.assertEqual(classify_path("WEBLyvra/index.html"), set())

    def test_diff_limit_marks_manual_review(self):
        topics, incomplete = candidate_from_compare(
            {"files": [{"filename": "README.md"}] * 300, "ahead_by": 301})
        self.assertTrue(incomplete)
        self.assertTrue(any("manuell" in x for x in topics))


class TodoPersistenceTests(unittest.TestCase):
    def test_never_change_checked_work(self):
        updated = update_issue_body(BODY, before=OLD, after=NEW,
                                    areas=["Music / Track Design / Speech"])
        self.assertIn("- [x] Historischer Test erledigt", updated)
        self.assertIn(f"<!-- LYVRA_NATIVE_HEAD:{NEW} -->", updated)
        self.assertIn("- [ ] **Native Änderung zur Bot-Relevanz prüfen**", updated)

    def test_no_relevance_does_not_invent_task(self):
        result = update_issue_body(BODY, before=OLD, after=NEW, areas=[])
        self.assertNotIn("Native Änderung zur Bot-Relevanz prüfen", result)
        self.assertIn(f"<!-- LYVRA_NATIVE_HEAD:{NEW} -->", result)

    def test_nochange_idempotent(self):
        self.assertEqual(update_issue_body(BODY, before=OLD, after=OLD,
                                           areas=["MUSIC"]), BODY)

    def test_stale_checkpoint_refused(self):
        with self.assertRaises(ValueError):
            update_issue_body(BODY, before=NEW, after=OLD, areas=["MUSIC"])

    def test_bad_commit_hash_refused(self):
        with self.assertRaises(ValueError):
            update_issue_body(BODY, before="invalid", after=NEW, areas=["MUSIC"])

    def test_missing_delimiter_refused(self):
        body = BODY.replace("## Arbeitsregeln", "## Anderes")
        with self.assertRaises(ValueError):
            update_issue_body(body, before=OLD, after=NEW, areas=["MUSIC"])


if __name__ == "__main__":
    unittest.main()
