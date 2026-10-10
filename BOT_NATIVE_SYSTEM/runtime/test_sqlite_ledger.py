import tempfile
import unittest
from pathlib import Path
from sqlite_ledger import append, read

EVENT={"event_id":"e1","timestamp_utc":"2026-10-10T01:00:00Z","facet":"livecircle","source_ref":"repo","source_sha":"a"*40,"cause":"test","decision":"record","effects":[],"validation":"TEST","relation":"KEEP_ACTIVE","supersedes":None,"rollback_ref":None}

class SQLiteLedgerTests(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bot.sqlite3"
            append(p,EVENT,{"livecircle"})
            self.assertEqual(read(p,{"livecircle"}),[EVENT])
    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bot.sqlite3"
            append(p,EVENT,{"livecircle"})
            with self.assertRaisesRegex(ValueError,"DUPLICATE_EVENT_ID"):
                append(p,EVENT,{"livecircle"})
            self.assertEqual(len(read(p,{"livecircle"})),1)
    def test_multiple_events(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"bot.sqlite3"
            append(p,EVENT,{"livecircle"})
            append(p,{**EVENT,"event_id":"e2"},{"livecircle"})
            self.assertEqual(len(read(p,{"livecircle"})),2)
    def test_foreign_facet_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"UNKNOWN_FACET"):
                append(Path(d)/"bot.sqlite3",EVENT,{"native_lyvra"})
    def test_invalid_provenance_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"INVALID_SOURCE_SHA"):
                append(Path(d)/"bot.sqlite3",{**EVENT,"source_sha":"invalid"},{"livecircle"})

    def test_symlink_read_denied(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'db';target.touch()
            link=Path(d)/'link';link.symlink_to(target)
            with self.assertRaisesRegex(ValueError,'SYMLINK_REJECTED'):
                read(link,{'livecircle'})
