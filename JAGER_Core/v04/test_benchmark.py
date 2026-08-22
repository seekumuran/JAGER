import unittest

from .benchmark import Benchmark


class FakeObservation:

    def __init__(self, status):
        self.status = status


class FakeExperience:

    def __init__(
        self,
        novelty,
        reward,
    ):
        self.novelty = novelty
        self.reward = reward


class FakeHunter:

    def __init__(self):
        self.experiments = [
            {
                "observation":
                    FakeObservation("NORMAL"),
                "experience":
                    FakeExperience(
                        0.2,
                        0.1,
                    ),
            },
            {
                "observation":
                    FakeObservation("FAILED"),
                "experience":
                    FakeExperience(
                        0.8,
                        1.0,
                    ),
            },
            {
                "observation":
                    FakeObservation("DEGRADED"),
                "experience":
                    FakeExperience(
                        0.5,
                        0.4,
                    ),
        ]


class FakePipeline:

    def candidates(self):
        return [
            object()
        ]

    def discoveries(self):
        return [
            object()
        ]


class TestBenchmark(unittest.TestCase):

    def test_evaluation(self):

        benchmark = Benchmark(
            FakeHunter(),
            FakePipeline(),
        )

        result = benchmark.evaluate()

        self.assertEqual(
            result.total_experiments,
            3,
        )

        self.assertEqual(
            result.total_candidates,
            1,
        )

        self.assertEqual(
            result.verified_discoveries,
            1,
        )

        self.assertEqual(
            result.normal_observations,
            1,
        )

        self.assertEqual(
            result.degraded_observations,
            1,
        )

        self.assertEqual(
            result.failed_observations,
            1,
        )

        self.assertAlmostEqual(
            result.average_novelty,
            0.5,
        )

        self.assertAlmostEqual(
            result.average_reward,
            0.5,
        )


if __name__ == "__main__":
    unittest.main()
