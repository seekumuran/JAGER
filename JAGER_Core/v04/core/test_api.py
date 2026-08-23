import unittest

from .api import JagerAPI
from .facade import Jager


class TestJagerAPI(
    unittest.TestCase
):

    def test_api_lifecycle(self):

        api = JagerAPI(
            Jager()
        )

        result = api.start()

        self.assertEqual(
            result["status"],
            "started",
        )

        experiment = (
            api.create_experiment(
                name="api-test",
                objective="test",
                target="mock",
            )
        )

        self.assertIsNotNone(
            experiment.experiment_id
        )

        health = api.health_status()

        self.assertTrue(
            health["healthy"]
        )

        api.stop()

    def test_diagnostics(self):

        api = JagerAPI(
            Jager()
        )

        summary = api.summary()

        self.assertIn(
            "version",
            summary,
        )

        self.assertIn(
            "experiments",
            summary,
        )


if __name__ == "__main__":
    unittest.main()
