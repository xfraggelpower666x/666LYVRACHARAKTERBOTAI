import unittest
from lyvra_source_guard import assess_lyvra_source, LYVRA_REPO
HEAD="a"*40
E={"repository":LYVRA_REPO,"branch":"lyvra","source_head":HEAD,"identity_authority":"WHOLE_LYVRA"}
class LYVRASourceTests(unittest.TestCase):
    def test_valid_source_never_approval(self):
        r=assess_lyvra_source(E,observed_lyvra_head=HEAD)
        self.assertEqual(r["status"],"SOURCE_ONLY")
        self.assertFalse(r["delivery"]);self.assertFalse(r["adoption"]);self.assertFalse(r["host"])
    def test_stale_blocks(self):
        self.assertIn("STALE_SOURCE",assess_lyvra_source(E,observed_lyvra_head="b"*40)["failures"])
    def test_foreign_authority_blocks(self):
        self.assertIn("FOREIGN_AUTHORITY_MISMATCH",assess_lyvra_source({**E,"repository":"elsewhere"},observed_lyvra_head=HEAD)["failures"])
    def test_persona_clone_blocks(self):
        self.assertIn("IDENTITY_AUTHORITY_MISMATCH",assess_lyvra_source({**E,"identity_authority":"BOT"},observed_lyvra_head=HEAD)["failures"])
    def test_malformed_blocks(self):
        self.assertEqual(assess_lyvra_source(None,observed_lyvra_head=HEAD)["status"],"BLOCKED")
