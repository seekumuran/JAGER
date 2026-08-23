import unittest

from .config import JagerConfig
from .facade import Jager
from .executor import JagerExecutor
from .runner import JagerRunner


class TestJagerRunner(
    unittest.TestCase
):

    def test_runner(self):

        config = JagerConfig(
            max_iterations=3,
            target_score=0.9,
        )

        jager = Jager(
            config
        )

        jager.start()

        experiment = (
            jager.create_experiment(
                name="runner-test",
                objective="evaluate",
                target="mock",
            )
        )

        executor = JagerExecutor(
            lambda action: {
                "value": action
            }
        )

        runner = JagerRunner(
            jager
        )

        results = runner.run(
            experiment.experiment_id,
            action=10,
            iterations=3,
            executor=executor.execute,
            evaluator=lambda output:
                0.95,
        )

        self.assertGreaterEqual(
            len(results),
            1,
        )

        self.assertTrue(
            results[0]["execution"]["success"]
        )

        jager.stop()


if __name__ == "__main__":

    unittest.main()
