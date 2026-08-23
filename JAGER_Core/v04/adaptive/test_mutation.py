import unittest

from .candidate import Candidate
from .mutation import (
    CandidateMutator,
)


class TestCandidateMutator(
    unittest.TestCase
):

    def test_numeric_mutation(self):

        parent = Candidate(
            candidate_id="parent",
            target="blackbox",
            parameters={
                "cpu_load": 50.0,
                "processes": 100,
            },
        )

        mutator = CandidateMutator(
            seed=42
        )

        child = mutator.mutate(
            parent,
            bounds={
                "cpu_load": (0.0, 100.0),
                "processes": (0, 200),
            },
        )

        self.assertEqual(
            child.target,
            "blackbox",
        )

        self.assertEqual(
            child.source,
            "mutation",
        )

        self.assertEqual(
            child.parent_id,
            "parent",
        )

    def test_many_mutations(self):

        parent = Candidate(
            "parent",
            "linux",
            {"processes": 100},
        )

        mutator = CandidateMutator()

        children = mutator.mutate_many(
            parent,
            10,
        )

        self.assertEqual(
            len(children),
            10,
        )

    def test_bounds(self):

        parent = Candidate(
            "parent",
            "blackbox",
            {"cpu": 100.0},
        )

        mutator = CandidateMutator(
            seed=1
        )

        child = mutator.mutate(
            parent,
            {
                "cpu": (0.0, 100.0)
            },
        )

        self.assertGreaterEqual(
            child.parameters["cpu"],
            0.0,
        )

        self.assertLessEqual(
            child.parameters["cpu"],
            100.0,
        )


if __name__ == "__main__":
    unittest.main()
