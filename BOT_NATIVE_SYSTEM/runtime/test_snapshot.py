import tempfile
import unittest
from pathlib import Path
from snapshot import snapshot
from sqlite_ledger import append

SHA="a"*40
M={"system_id":"666LYVRA-CHARACTER-BOT-CORE-001","status":"DEV_NOT_PROMOTED","identity_authority":"native_LYVRA_external","source_branch":"dev","discord_login_allowed":False,"lyvra_worker_writes_allowed":False,"facets":["livecircle"]}
P={"schema":"BOT_CURRENT_POINTER_v1","status":"DEV_CANDIDATE_ONLY","source_baseline_commit":SHA,"canonical_branch":"dev","discord_deployment":False,"runtime_head_selected":False}
E={"event_id":"one","timestamp_utc":"2026-10-10T00:00:00Z","facet":"livecircle","source_ref":"github","source_sha":SHA,"cause":"test","decision":"keep","effects":[],"validation":"TEST","relation":"KEEP_ACTIVE","supersedes":None,"rollback_ref":None}

class SnapshotTests(unittest.TestCase):
    def test_empty_still_partial(self):
        with tempfile.TemporaryDirectory() as d:
            r=snapshot(M,P,SHA,"dev",Path(d)/"events.db")
            self.assertEqual((r["status"],r["events"]),("PARTIAL",0))
    def test_reads_scoped_events(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"events.db";append(p,E,{"livecircle"})
            r=snapshot(M,P,SHA,"dev",p)
            self.assertEqual(r["facets"]["livecircle"]["latest_event_id"],"one")
            self.assertFalse(r["release_ready"])
    def test_branch_mismatch_shortcircuits(self):
        with tempfile.TemporaryDirectory() as d:
            r=snapshot(M,P,SHA,"wrong",Path(d)/"events.db")
            self.assertEqual(r["status"],"BLOCKED")
    def test_never_assumes_native_authority(self):
        with tempfile.TemporaryDirectory() as d:
            r=snapshot(M,P,SHA,"dev",Path(d)/"events.db")
            self.assertFalse(r["native_lyvra_rehydrated"])

    def test_corrupt_sqlite_blocks_without_crash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'events.db'
            p.write_text('not a sqlite database')
            result=snapshot(M,P,SHA,'dev',p)
            self.assertEqual(result['status'],'BLOCKED')
            self.assertIn('LEDGER_READBACK_FAILED',result['blockers'])
