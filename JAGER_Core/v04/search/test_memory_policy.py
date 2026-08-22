import tempfile
import unittest
from pathlib import Path

from ..memory import ExperimentMemory
from .memory_policy import (
    MemoryGuidedPolicy,
)


class TestMemoryGuidedPolicy(
    unittest.TestCase
):

    def test_empty_memory_preserves_candidates(self):

        with tempfile.TemporaryDirectory() as directory:

            memory = ExperimentMemory(
                Path(directory)
                / "memory.json"
            )

            policy = MemoryGuidedPolicy(
                memory
            )

            candidates = [
                {"type": "probe"},
                {"type": "inspect"},
            ]

            ranked = policy.rank(
                candidates
            )

            self.assertEqual(
                len(ranked),
                2,
            )

    def test_history_changes_ranking(self):

        with tempfile.TemporaryDirectory() as directory:

            memory = ExperimentMemory(
                Path(directory)
                / "memory.json"
            )

            memory.add(
                {
                    "action": {
                        "type": "probe"
                    },
                    "reward": 10.0,
                    "novelty": 0.0,
                }
            )

            memory.add(
                {
                    "action": {
                        "type": "inspect"
                    },
                    "reward": 0.0,
                    "novelty": 0.0,
                }
            )

            policy = MemoryGuidedPolicy(
                memory
            )

            candidates = [
                {"type": "inspect"},
                {"type": "probe"},
            ]

            ranked = policy.rank(
                candidates
            )

            self.assertEqual(
                ranked[0]["type"],
                "probe",
            )


if __name__ == "__main__":
    unittest.main()
