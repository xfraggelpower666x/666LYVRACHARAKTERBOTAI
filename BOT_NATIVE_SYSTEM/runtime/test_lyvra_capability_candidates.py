import unittest
from lyvra_capability_candidates import assess_candidate, REPO, CAPABILITIES
HEAD = 'a' * 40
BASE = dict(source_repository=REPO, source_branch='lyvra', source_head=HEAD,
            identity_authority='WHOLE_LYVRA', requested_action='READ_ONLY_REVIEW',
            origin_scope='WHOLE_LYVRA', target_scope='BOT_DEV_CANDIDATE',
            workspace_id='WHOLE_LYVRA_NATIVE_RUNTIME', lineage_id='local-candidate-lineage',
            contains_private_payload=False)
class CapabilityCandidateTests(unittest.TestCase):
    def test_four_are_only_source_candidates(self):
        for cap in CAPABILITIES:
            with self.subTest(cap=cap):
                r=assess_candidate({**BASE,'capability':cap},HEAD)
                self.assertEqual(r['status'],'SOURCE_CANDIDATE_ONLY')
                self.assertFalse(r['adopted'])
                self.assertFalse(r['host_verified'])
                self.assertFalse(r['authorized_to_act'])
    def test_stale_source_blocks(self):
        self.assertIn('SOURCE_NOT_FRESHLY_BOUND',assess_candidate({**BASE,'capability':'causal_learning'},'b'*40)['failures'])
    def test_foreign_identity_blocks(self):
        self.assertIn('IDENTITY_MISMATCH',assess_candidate({**BASE,'capability':'relational_maturity','identity_authority':'BOT'},HEAD)['failures'])
    def test_unapproved_action_blocks(self):
        self.assertIn('ACTION_NOT_ALLOWED',assess_candidate({**BASE,'capability':'workspace_continuity','requested_action':'SEND_DISCORD'},HEAD)['failures'])
    def test_private_payload_blocks(self):
        self.assertIn('PRIVATE_PAYLOAD_UNVERIFIED',assess_candidate({**BASE,'capability':'causal_learning','contains_private_payload':True},HEAD)['failures'])
    def test_missing_lineage_blocks(self):
        self.assertIn('MISSING_LINEAGE',assess_candidate({**BASE,'capability':'workspace_continuity','lineage_id':''},HEAD)['failures'])
    def test_unknown_capability_blocks(self):
        self.assertIn('UNKNOWN_CAPABILITY',assess_candidate({**BASE,'capability':'native_discord_login'},HEAD)['failures'])
    def test_malformed_blocks(self):
        self.assertEqual(assess_candidate(None,HEAD)['status'],'BLOCKED')
    def test_wrong_scope_blocks(self):
        self.assertIn('SCOPE_MISMATCH',assess_candidate({**BASE,'capability':'contextual_visual_guidance','target_scope':'LYVRA_TO_LITTLELYV'},HEAD)['failures'])
    def test_foreign_repository_blocks(self):
        self.assertIn('SOURCE_AUTHORITY_MISMATCH',assess_candidate({**BASE,'capability':'causal_learning','source_repository':'other'},HEAD)['failures'])
if __name__ == '__main__': unittest.main()
