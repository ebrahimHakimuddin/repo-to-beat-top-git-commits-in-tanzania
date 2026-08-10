import unittest

from poc import Contributor, rankings, simulate


class PocTests(unittest.TestCase):
    def test_raw_count_includes_synthetic_events(self):
        contributor = Contributor("test", 3, 45_000)
        self.assertEqual(contributor.raw_count, 45_003)

    def test_quality_score_caps_repetitive_activity(self):
        contributor = Contributor("test", 3, 45_000)
        self.assertEqual(contributor.quality_aware_score, 28)

    def test_inflated_account_tops_raw_but_not_quality_ranking(self):
        contributors = simulate(45_000)
        self.assertEqual(rankings(contributors, "raw")[0].name, "POC account")
        self.assertNotEqual(rankings(contributors, "quality")[0].name, "POC account")

    def test_negative_events_are_rejected(self):
        with self.assertRaises(ValueError):
            simulate(-1)


if __name__ == "__main__":
    unittest.main()
