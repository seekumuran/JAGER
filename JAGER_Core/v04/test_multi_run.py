import unittest

from .multi_run import (
    MultiRunExperiment,
)


class FakeSummary:

    def __init__(
        self,
        run_id,
        seed,
    ):
        self.run_id = run_id
        self.seed = seed

        self.experiments = 4
        self.candidates = 2
        self.verified = 1

        self.normal = 2
        self.degraded = 1
        self.failed = 1


class FakeRecord:

    reward = 1.0
    novelty = 0.5


class FakeRun:

    def __init__(
        self,
        summary,
    ):
        self.summary = summary
        self.records = [
            FakeRecord(),
            FakeRecord(),
        ]


class FakeExecutor:

    def __init__(
        self,
        summary,
    ):
        self.run = FakeRun(
            summary
        )


class FakeRuntime:

    def __init__(
        self,
        seed,
    ):
        self.seed = seed

        self.executor = FakeExecutor(
            FakeSummary(
                f"run-{seed}",
                seed,
            )
        )

    def run_protocol(
        self,
        target_name,
        save=True,
    ):
        return {
            "state": "FINALIZED"
        }


def runtime_factory(seed):
    return FakeRuntime(seed)


class TestMultiRun(
    unittest.TestCase
):

    def test_multiple_runs(self):

        experiment = MultiRunExperiment(
            runtime_factory,
            "blackbox",
            [1, 2, 3],
        )

        results = experiment.run()

        self.assertEqual(
            len(results),
            3,
        )

        summary = (
            experiment.summary()
        )

        self.assertEqual(
            summary["runs"],
            3,
        )

        self.assertEqual(
            summary[
                "total_experiments"
            ],
            12,
        )

        self.assertEqual(
            summary[
                "total_verified"
            ],
            3,
        )

    def test_average_metrics(self):

        experiment = MultiRunExperiment(
            runtime_factory,
            "blackbox",
            [1],
        )

        experiment.run()

        summary = (
            experiment.summary()
        )

        self.assertAlmostEqual(
            summary[
                "average_reward"
            ],
            1.0,
        )

        self.assertAlmostEqual(
            summary[
                "average_novelty"
            ],
            0.5,
        )


if __name__ == "__main__":
    unittest.main()
