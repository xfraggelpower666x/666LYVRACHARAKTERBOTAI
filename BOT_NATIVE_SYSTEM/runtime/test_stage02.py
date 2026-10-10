import tempfile
import unittest
from pathlib import Path
from rehydration_stage02 import rehydrate
from facet_ledger import append_event, load_events

BASE='a'*40
M={'system_id':'666LYVRA-CHARACTER-BOT-CORE-001','status':'DEV_NOT_PROMOTED','identity_authority':'native_LYVRA_external','source_branch':'dev','discord_login_allowed':False,'lyvra_worker_writes_allowed':False}
P={'schema':'BOT_CURRENT_POINTER_v1','status':'DEV_CANDIDATE_ONLY','source_baseline_commit':BASE,'canonical_branch':'dev','discord_deployment':False,'runtime_head_selected':False}
E={'event_id':'e1','timestamp_utc':'2026-10-10T00:00:00Z','facet':'livecircle','source_ref':'repo','source_sha':BASE,'cause':'test','decision':'retain','effects':[],'validation':'TEST','relation':'KEEP_ACTIVE','supersedes':None,'rollback_ref':None}

class Stage02Tests(unittest.TestCase):
    def test_partial_not_release(self):
        self.assertEqual(rehydrate(M,P,BASE,'dev')['status'],'PARTIAL')
    def test_branch_blocks(self):
        self.assertEqual(rehydrate(M,P,BASE,'main')['status'],'BLOCKED')
    def test_head_blocks(self):
        self.assertIn('INVALID_OBSERVED_HEAD',rehydrate(M,P,'x','dev')['blockers'])
    def test_authority_blocks(self):
        self.assertIn('NATIVE_IDENTITY_BOUNDARY_MISMATCH',rehydrate({**M,'identity_authority':'bot'},P,BASE,'dev')['blockers'])
    def test_append_read(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'e.jsonl';append_event(path,E,{'livecircle'})
            self.assertEqual(load_events(path,{'livecircle'}),[E])
    def test_other_facet_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'UNKNOWN_FACET'):
                append_event(Path(d)/'e.jsonl',E,{'codeforge'})
    def test_invalid_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'INVALID_SOURCE_SHA'):
                append_event(Path(d)/'e.jsonl',{**E,'source_sha':'bad'},{'livecircle'})
    def test_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'e.jsonl';p.write_text('{bad\n')
            with self.assertRaisesRegex(ValueError,'CORRUPT_EVENT_LINE'):
                load_events(p,{'livecircle'})
    def test_duplicates_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'e.jsonl';append_event(p,E,{'livecircle'})
            with self.assertRaisesRegex(ValueError,'DUPLICATE_EVENT_ID'):
                append_event(p,E,{'livecircle'})

    def test_two_sequential_events(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'e.jsonl'
            append_event(p,E,{'livecircle'})
            append_event(p,{**E,'event_id':'e2'},{'livecircle'})
            self.assertEqual(len(load_events(p,{'livecircle'})),2)
    def test_lockfile_created(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'e.jsonl'
            append_event(p,E,{'livecircle'})
            self.assertTrue(Path(str(p)+'.lock').exists())
