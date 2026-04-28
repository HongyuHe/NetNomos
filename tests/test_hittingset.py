from __future__ import annotations

import unittest

from netnomos.learners.hittingset import HittingSetLearner


class HittingSetLearnerTest(unittest.TestCase):
    def test_enumeration_completes_without_timeout(self) -> None:
        learner = HittingSetLearner(max_clause_size=2, max_rules=16)
        covers, metadata = learner.enumerate_minimal_hitting_sets([
            {0},
            {1},
        ])

        self.assertEqual(covers, [{0, 1}])
        self.assertFalse(metadata["search_stopped_early"])
        self.assertEqual(metadata["stop_reason"], "complete")

    def test_stall_timeout_returns_partial_solutions(self) -> None:
        call_count = 0

        def clock() -> float:
            nonlocal call_count
            call_count += 1
            if call_count <= 24:
                return 0.0
            return 10.0

        learner = HittingSetLearner(
            max_clause_size=3,
            max_rules=64,
            stall_timeout=1.0,
            clock=clock,
        )
        covers, metadata = learner.enumerate_minimal_hitting_sets([
            {0, 1, 2},
            {0, 3, 4},
            {1, 3, 5},
            {2, 4, 5},
            {0, 5},
            {1, 4},
        ])

        self.assertGreaterEqual(len(covers), 1)
        self.assertTrue(metadata["search_stopped_early"])
        self.assertEqual(metadata["stop_reason"], "stall-timeout")
        self.assertEqual(metadata["stall_timeout_seconds"], 1.0)


if __name__ == "__main__":
    unittest.main()
