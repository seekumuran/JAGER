import unittest

from .experiment_runtime import (
    ExperimentRuntime,
)

from .termination import (
    TerminationController,
)

from .runtime_controller import (
    RuntimeController,
)


class TestExperimentRuntime(
    unittest.TestCase
):

    def test_end_to_end_runtime(self):

        runtime = ExperimentRuntime(
            controller=RuntimeController(
                termination=
                    TerminationController(
                        maximum_iterations=2
                    )
            )
        )

        experiment = runtime.create(
            name="demo",
            objective="evaluate",
            target="mock",
        )

        runtime.start(
            experiment.experiment_id
        )

        context = runtime.begin_iteration(
            experiment.experiment_id,
            1,
        )

        record = runtime.begin_execution(
            action={
                "type": "probe"
            },
            iteration=1,
            experiment_id=
                experiment.experiment_id,
        )

        result = runtime.complete_execution(
            record,
            output={
                "score": 0.8
            },
        )

        self.assertTrue(
            result.success
        )

        self.assertEqual(
            context.iteration,
            1,
        )

        decision = runtime.evaluate(
            experiment.experiment_id,
            iteration=1,
            score=0.8,
        )

        self.assertFalse(
            decision.should_stop
        )

        runtime.begin_iteration(
            experiment.experiment_id,
            2,
        )

        decision = runtime.evaluate(
            experiment.experiment_id,
            iteration=2,
            score=0.8,
        )

        self.assertTrue(
            decision.should_stop
        )

        self.assertEqual(
            experiment.status,
            "completed",
        )


if __name__ == "__main__":
    unittest.main()
