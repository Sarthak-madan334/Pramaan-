import unittest

from engine.grounded_bullet import BulletPlan, Fact, FactLedger, LedgerError, render_bullet, validate_bullet


class GroundedBulletTests(unittest.TestCase):
    def setUp(self):
        self.ledger = FactLedger(
            [
                Fact("f1", "c1", "action", "Built", "resume", "resume:project:1"),
                Fact("f2", "c1", "object", "a search feature", "resume", "resume:project:1"),
                Fact("f3", "c1", "technology", "Python", "resume", "resume:project:1"),
                Fact("f4", "c1", "outcome", None, "placeholder"),
                Fact("f5", "c2", "outcome", "reduced query time", "user_stated", "answer-1"),
            ]
        )

    def test_valid_plan_renders_and_accepts_only_exact_text(self):
        plan = BulletPlan("c1", "f1", "f2", "f3")
        bullet = render_bullet(self.ledger, plan)
        self.assertEqual(bullet, "Built a search feature using Python.")
        self.assertTrue(validate_bullet(bullet, self.ledger, plan))
        self.assertFalse(validate_bullet("Built a search feature using Python for 500 users.", self.ledger, plan))

    def test_missing_or_cross_claim_evidence_is_rejected(self):
        for plan in (
            BulletPlan("c1", "f1", "f2", outcome_fact_id="f4"),
            BulletPlan("c1", "f1", "f2", outcome_fact_id="f5"),
            BulletPlan("c1", "f1", "unknown"),
        ):
            with self.assertRaises(LedgerError):
                render_bullet(self.ledger, plan)

    def test_ledger_requires_evidence_for_derived_facts(self):
        with self.assertRaises(LedgerError):
            FactLedger([Fact("x", "c1", "technology", "Python", "repo_derived")])

    def test_duplicate_ids_and_multiline_values_fail(self):
        with self.assertRaises(LedgerError):
            FactLedger([Fact("x", "c1", "action", "Built", "resume", "resume:1")] * 2)
        bad = FactLedger(
            [Fact("a", "c", "action", "Built", "resume", "resume:1"), Fact("o", "c", "object", "item\nextra", "resume", "resume:1")]
        )
        with self.assertRaises(LedgerError):
            render_bullet(bad, BulletPlan("c", "a", "o"))


if __name__ == "__main__":
    unittest.main()
