import unittest

from .candidates import Candidate
from .verifier import CandidateVerifier


class DeterministicTarget:

    def __init__(self, status):
        self.status = status

    def observe(self, **inputs):
        return {
            "inputs": inputs,
            "telemetry": {},
            "status": self.status,
        }


class TestCandidateVerifier(
    unittest.TestCase
):

    def make_candidate(self):
        return Candidate(
            candidate_id="candidate-1",
            experiment_id="experiment-1",
            inputs={
                "cpu_load": 95,
                "memory_load": 95,
            },
            status="FAILED",
            novelty=0.9,
            reward=1.0,
        )

    def test_confirmed_failure(self):

        verifier = CandidateVerifier(
            DeterministicTarget(
                "FAILED"
            ),
            attempts=3,
        )

        candidate = (
            self.make_candidate()
        )

        result = verifier.verify(
            candidate
        )

        self.assertTrue(
            result["confirmed"]
        )

        self.assertTrue(
            candidate.verified
        )

        self.assertEqual(
            candidate.verification_attempts,
            3,
        )

    def test_unconfirmed_failure(self):

        verifier = CandidateVerifier(
            DeterministicTarget(
                "NORMAL"
            ),
            attempts=3,
        )

        candidate = (
            self.make_candidate()
        )

        result = verifier.verify(
            candidate
        )

        self.assertFalse(
            result["confirmed"]
        )

        self.assertFalse(
            candidate.verified
        )


if __name__ == "__main__":
    unittest.main()
