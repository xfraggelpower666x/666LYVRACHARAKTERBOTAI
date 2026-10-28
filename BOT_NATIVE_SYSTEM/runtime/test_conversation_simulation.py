import unittest
from conversation_simulation import simulate_conversation
from test_semantic_acceptance import four, HEAD
T={'kind':'CONTEXT','workspace_id':'WHOLE_LYVRA_NATIVE_RUNTIME','lineage_id':'bot-27','contains_private_payload':False,'requested_action':'READ_ONLY_REVIEW'}
class SimulationTests(unittest.TestCase):
    def test_context_and_counterexample(self):
        x=simulate_conversation(four(),HEAD,[T,{**T,'kind':'COUNTEREXAMPLE'}])
        self.assertEqual(x['status'],'SIMULATION_REVIEWED')
        self.assertFalse(x['discord_enabled']);self.assertFalse(x['authorized_to_act'])
    def test_cross_lineage_blocks(self):
        self.assertIn('CONTEXT_BOUNDARY_VIOLATION',simulate_conversation(four(),HEAD,[{**T,'lineage_id':'another'}])['reasons'])
    def test_cross_workspace_blocks(self):
        self.assertIn('CONTEXT_BOUNDARY_VIOLATION',simulate_conversation(four(),HEAD,[{**T,'workspace_id':'other'}])['reasons'])
    def test_discord_action_blocks(self):
        self.assertIn('ACTION_NOT_ALLOWED',simulate_conversation(four(),HEAD,[{**T,'requested_action':'SEND_DISCORD'}])['reasons'])
    def test_private_counterexample_blocks(self):
        self.assertIn('PRIVATE_CONTENT_NOT_ALLOWED',simulate_conversation(four(),HEAD,[{**T,'kind':'COUNTEREXAMPLE','contains_private_payload':True}])['reasons'])
    def test_host_claim_blocks(self):
        self.assertIn('HOST_CLAIM_NOT_PROOF',simulate_conversation(four(),HEAD,[{**T,'asserted_host_success':True}])['reasons'])
    def test_unknown_kind_blocks(self):
        self.assertIn('UNKNOWN_TURN_KIND',simulate_conversation(four(),HEAD,[{**T,'kind':'AUTONOMOUS_ACTION'}])['reasons'])
    def test_empty_blocks(self):
        self.assertIn('INVALID_TURN_SET',simulate_conversation(four(),HEAD,[])['reasons'])
    def test_malformed_blocks(self):
        self.assertIn('INVALID_TURN',simulate_conversation(four(),HEAD,[None])['reasons'])
    def test_stale_source_blocks(self):
        self.assertEqual(simulate_conversation(four(),'b'*40,[T])['status'],'BLOCKED')
if __name__=='__main__': unittest.main()
