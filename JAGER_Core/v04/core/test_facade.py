import unittest

from .config import JagerConfig
from .facade import Jager


class TestJager(
    unittest.TestCase
):

    def test_full_flow(self):

        config = JagerConfig(
            max_iterations=2,
            target_score=0.9,
        )

        jager = Jager(
            config
        )

        started = jager.start()

        self.assertEqual(
            started["status"],
            "started",
        )

        experiment = (
            jager.create_experiment(
                name="demo",
                objective="evaluate",
                target="mock",
            )
        )

        context, record, _ = (
            jager.execute(
                experiment_id=
                    experiment.experiment_id,
                iteration=1,
                action={
                    "type": "probe"
                },
            )
        )

        result = jager.complete(
            record,
            output={
                "value": 1
            },
        )

        self.assertTrue(
            result.success
        )

        decision = jager.evaluate(
            experiment_id=
                experiment.experiment_id,
            iteration=1,
            score=0.95,
        )

        self.assertTrue(
            decision.should_stop
        )

        self.assertEqual(
            experiment.status,
            "completed",
        )

        jager.stop()

    def test_snapshot(self):

        jager = Jager()

        snapshot = jager.snapshot()

        self.assertIn(
            "config",
            snapshot,
        )

        self.assertIn(
            "runtime",
            snapshot,
        )


if __name__ == "__main__":
    unittest.main()
