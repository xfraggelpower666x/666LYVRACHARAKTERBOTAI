"""Offline regression checks for the isolated read-only LYVRA Discord bridge."""
import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from native_bridge.livecircle import LiveCircleStore, RELATION_STATES
from native_bridge.source import NativeSource, NativeSnapshot, PUBLIC_CONTEXT_PATHS, POINTER_PATH, presentation_context


class FakeSource(NativeSource):
    def __init__(self, broken=(), moving=False):
        super().__init__(token="")
        self.broken = set(broken)
        self.moving = moving
        self.head_calls = 0

    def head(self):
        self.head_calls += 1
        if self.moving and self.head_calls > 1:
            return "b" * 40
        return "a" * 40

    def read(self, path, sha):
        if path in self.broken:
            raise ValueError("missing")
        return '{}' if path == POINTER_PATH else 'verified public test text ' + path


class NativeTests(unittest.TestCase):
    def test_snapshot_is_never_full_rehydration(self):
        result = FakeSource().snapshot()
        self.assertEqual(result.public_state, "PUBLIC_CORE_READ")
        self.assertEqual(result.whole_state, "PARTIAL/READBACK_PENDING")
        self.assertTrue(result.pointer_read)
        self.assertEqual(len(result.public_documents), len(PUBLIC_CONTEXT_PATHS))

    def test_missing_pointer_degrades(self):
        result = FakeSource(broken=(POINTER_PATH,)).snapshot()
        self.assertEqual(result.public_state, "PARTIAL")
        self.assertFalse(result.pointer_read)

    def test_missing_domain_degrades(self):
        result = FakeSource(broken=(PUBLIC_CONTEXT_PATHS["identity"],)).snapshot()
        self.assertEqual(result.public_state, "PARTIAL")

    def test_head_change_degrades(self):
        result = FakeSource(moving=True).snapshot()
        self.assertIn("HEAD_CHANGED_DURING_READ", result.errors)
        self.assertEqual(result.public_state, "PARTIAL")

    def test_source_restricts_authority(self):
        with self.assertRaises(ValueError):
            NativeSource(branch="main")
        with self.assertRaises(ValueError):
            NativeSource(repository="example/foreign")

    def test_context_discloses_partial(self):
        sample = FakeSource().snapshot()
        context = presentation_context(sample)
        self.assertIn("PUBLIC CONTEXT IS PARTIAL", context)
        self.assertNotIn("WHOLE_REHYDRATED", context)

    def test_reader_integrity_is_not_a_preset(self):
        class FakeApi(NativeSource):
            def _json(self, route):
                blob = b"hello"
                sha = hashlib.sha1(b"blob 5\0hello").hexdigest()
                return {"encoding": "base64", "type": "file",
                        "content": base64.b64encode(blob).decode(), "sha": sha}
        self.assertEqual(FakeApi(token="").read("file.md", "f" * 40), "hello")

    def test_bad_blob_fails(self):
        class FakeApi(NativeSource):
            def _json(self, route):
                return {"encoding": "base64", "type": "file", "content": "aGVsbG8=", "sha": "0"*40}
        with self.assertRaises(ValueError):
            FakeApi(token="").read("file.md", "f"*40)


class LiveCircleTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.store = LiveCircleStore(str(Path(self.d.name) / "local.sqlite3"))

    def tearDown(self):
        self.d.cleanup()

    def test_relation_states(self):
        self.assertEqual(len(RELATION_STATES), 6)
        for state in RELATION_STATES:
            self.assertGreater(self.store.record(guild_id=1, author_id=2,
                                                 state=state, meaning=state), 0)
        self.assertEqual(self.store.count(1), 6)

    def test_reject_unknown_state(self):
        with self.assertRaises(ValueError):
            self.store.record(guild_id=1, author_id=2, state="CURRENT", meaning="x")

    def test_guild_isolation(self):
        self.store.record(guild_id=1, author_id=2, meaning="private-for-one")
        self.assertEqual(self.store.count(2), 0)
        self.assertEqual(self.store.recent(2), [])

    def test_supersession_scope(self):
        event = self.store.record(guild_id=1, author_id=2, meaning="old")
        with self.assertRaises(ValueError):
            self.store.record(guild_id=2, author_id=2, meaning="no", supersedes=event)
        new = self.store.record(guild_id=1, author_id=2, meaning="new",
                                state="SUPERSEDE", supersedes=event)
        self.assertNotEqual(event, new)

    def test_limit_and_empty_validation(self):
        for message in [" ", "a"*601]:
            with self.assertRaises(ValueError):
                self.store.record(guild_id=1, author_id=2, meaning=message)

    def test_forget_scoped_to_guild(self):
        event = self.store.record(guild_id=1, author_id=2, meaning="erase me")
        self.assertFalse(self.store.forget(2, event))
        self.assertEqual(self.store.count(1), 1)
        self.assertTrue(self.store.forget(1, event))
        self.assertEqual(self.store.count(1), 0)

    def test_no_automatic_authority_update(self):
        self.store.record(guild_id=1, author_id=2, meaning="Learning candidate")
        rows = self.store.recent(1)
        self.assertEqual(rows[0]["evidence_class"], "DISCORD_OWNER_NOTE")
        self.assertNotIn("pointer", rows[0])
        self.assertNotIn("authority", rows[0])


if __name__ == "__main__":
    unittest.main()
