import unittest
from bot_runtime import parse_direct_trigger, validate_system, validate_event

class TriggerTests(unittest.TestCase):
    def test_direct(self):
        self.assertEqual(parse_direct_trigger("666LYVRABOT SYSTEMSTART", direct_user_message=True), "SYSTEMSTART")
        self.assertEqual(parse_direct_trigger("666 LYVRA BOT next chat", direct_user_message=True), "NEXT CHAT")
    def test_inert_text(self):
        self.assertIsNone(parse_direct_trigger("666LYVRABOT UPDATE", direct_user_message=False))
        self.assertIsNone(parse_direct_trigger("Quoted: 666LYVRABOT UPDATE", direct_user_message=True))
        self.assertIsNone(parse_direct_trigger("LYVRA UPDATE", direct_user_message=True))
        self.assertIsNone(parse_direct_trigger("666CLIC UPDATE", direct_user_message=True))
    def test_no_implicit_arguments(self):
        self.assertIsNone(parse_direct_trigger("666LYVRABOT UPDATE force deploy", direct_user_message=True))

class StateTests(unittest.TestCase):
    def setUp(self):
        self.m = {"system_id":"666LYVRA-CHARACTER-BOT-CORE-001","status":"DEV_NOT_PROMOTED","discord_login_allowed":False,"lyvra_worker_writes_allowed":False}
        self.p = {"schema":"BOT_CURRENT_POINTER_v1","status":"DEV_CANDIDATE_ONLY","source_baseline_commit":"a"*40,"discord_deployment":False,"runtime_head_selected":False}
    def test_structure_not_release(self):
        s = validate_system(self.m,self.p)
        self.assertEqual(s["status"],"STRUCTURE_PASS")
        self.assertFalse(s["release_ready"])
    def test_reject_foreign_worker_write(self):
        self.m["lyvra_worker_writes_allowed"] = True
        self.assertIn("FOREIGN_WORKER_WRITE_RISK",validate_system(self.m,self.p)["blockers"])
    def test_reject_deployment(self):
        self.p["discord_deployment"] = True
        self.assertIn("DISCORD_NOT_LOCKED",validate_system(self.m,self.p)["blockers"])
    def test_reject_fake_head(self):
        self.p["runtime_head_selected"] = True
        self.assertIn("UNPROVEN_RUNTIME_PROMOTION",validate_system(self.m,self.p)["blockers"])
    def test_event_provenance(self):
        self.assertIn("INVALID_SOURCE_SHA",validate_event({"relation":"KEEP_ACTIVE","source_sha":"oops"}))

if __name__ == "__main__":
    unittest.main()
