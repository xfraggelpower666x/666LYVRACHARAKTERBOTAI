import unittest
from semantic_acceptance import review_capability_set
from lyvra_capability_candidates import CAPABILITIES, REPO
HEAD='a'*40
BASE=dict(source_repository=REPO,source_branch='lyvra',source_head=HEAD,identity_authority='WHOLE_LYVRA',requested_action='READ_ONLY_REVIEW',origin_scope='WHOLE_LYVRA',target_scope='BOT_DEV_CANDIDATE',workspace_id='WHOLE_LYVRA_NATIVE_RUNTIME',lineage_id='bot-27',contains_private_payload=False)
def four(): return [{**BASE,'capability':c} for c in sorted(CAPABILITIES)]
class AcceptanceTests(unittest.TestCase):
    def test_source_only(self):
        r=review_capability_set(four(),HEAD)
        self.assertEqual(r['status'],'SOURCE_SET_REVIEWED')
        for k in ('adopted','host_verified','authorized_to_act','discord_enabled'): self.assertFalse(r[k])
    def test_incomplete(self): self.assertIn('CAPABILITY_SET_INCOMPLETE',review_capability_set(four()[:-1],HEAD)['reasons'])
    def test_duplicate(self):
        a=four(); a[-1]=a[0]
        self.assertIn('CAPABILITY_SET_MISMATCH',review_capability_set(a,HEAD)['reasons'])
    def test_cross_lineage(self):
        a=four(); a[-1]={**a[-1],'lineage_id':'other'}
        self.assertIn('CROSS_LINEAGE_MIX',review_capability_set(a,HEAD)['reasons'])
    def test_stale_head(self): self.assertEqual(review_capability_set(four(),'b'*40)['status'],'BLOCKED')
    def test_mixed_heads(self):
        a=four(); a[-1]={**a[-1],'source_head':'b'*40}
        self.assertIn('MIXED_SOURCE_HEADS',review_capability_set(a,HEAD)['reasons'])
    def test_discord_action(self):
        a=four(); a[0]={**a[0],'requested_action':'SEND_DISCORD'}
        self.assertIn('ACTION_NOT_ALLOWED',review_capability_set(a,HEAD)['reasons'])
    def test_private_candidate(self):
        a=four(); a[0]={**a[0],'contains_private_payload':True}
        self.assertIn('PRIVATE_PAYLOAD_UNVERIFIED',review_capability_set(a,HEAD)['reasons'])
    def test_feedback_claim(self): self.assertIn('FEEDBACK_NOT_EVIDENCE',review_capability_set(four(),HEAD,feedback={'kind':'HOST_PASS','contains_private_payload':False})['reasons'])
    def test_private_counterexample(self): self.assertIn('PRIVATE_FEEDBACK_UNVERIFIED',review_capability_set(four(),HEAD,feedback={'kind':'COUNTEREXAMPLE','contains_private_payload':True})['reasons'])
    def test_public_counterexample(self): self.assertEqual(review_capability_set(four(),HEAD,feedback={'kind':'COUNTEREXAMPLE','contains_private_payload':False})['status'],'SOURCE_SET_REVIEWED')
    def test_malformed(self): self.assertEqual(review_capability_set(None,HEAD)['status'],'BLOCKED')
if __name__ == '__main__': unittest.main()
