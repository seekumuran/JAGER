import unittest

from .candidate import Candidate
from .candidate_pool import (
    CandidatePool,
)
from .candidate_id import (
    CandidateID,
)


class TestCandidatePool(
    unittest.TestCase
):

    def test_add_and_get(self):

        pool = CandidatePool()

        candidate = Candidate(
            candidate_id="cand-1",
            target="blackbox",
            parameters={
                "cpu_load": 50
            },
        )

        pool.add(candidate)

        self.assertEqual(
            pool.size(),
            1,
        )

        self.assertEqual(
            pool.get(
                "cand-1"
            ),
            candidate,
        )

    def test_maximum_size(self):

        pool = CandidatePool(
            maximum_size=2
        )

        for index in range(5):

            pool.add(
                Candidate(
                    candidate_id=
                        f"cand-{index}",
                    target="blackbox",
                    parameters={
                        "x": index
                    },
                )
            )

        self.assertEqual(
            pool.size(),
            2,
        )

    def test_candidate_id(self):

        first = CandidateID.generate(
            "blackbox",
            {
                "cpu": 50,
                "memory": 70,
            },
        )

        second = CandidateID.generate(
            "blackbox",
            {
                "cpu": 50,
                "memory": 70,
            },
        )

        self.assertEqual(
            first,
            second,
        )

    def test_action_conversion(self):

        candidate = Candidate(
            candidate_id="cand-1",
            target="linux",
            parameters={
                "operation":
                    "observe"
            },
        )

        action = (
            candidate.to_action()
        )

        self.assertEqual(
            action["type"],
            "probe",
        )

        self.assertEqual(
            action["parameters"][
                "operation"
            ],
            "observe",
        )


if __name__ == "__main__":
    unittest.main()
