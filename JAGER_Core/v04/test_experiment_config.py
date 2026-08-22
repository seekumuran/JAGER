import unittest

from .experiment_config import (
    ExperimentConfig,
)


class TestExperimentConfig(unittest.TestCase):

    def test_defaults(self):
        config = ExperimentConfig()

        self.assertEqual(
            config.seed,
            42,
        )

        self.assertEqual(
            config.budget,
            100,
        )

        self.assertEqual(
            config.version,
            "0.4.0",
        )

    def test_serialization(self):
        config = ExperimentConfig(
            seed=123,
            budget=20,
            target_name="blackbox",
        )

        data = config.to_dict()

        restored = (
            ExperimentConfig.from_dict(
                data
            )
        )

        self.assertEqual(
            restored.to_dict(),
            data,
        )

    def test_invalid_budget(self):
        with self.assertRaises(
            ValueError
        ):
            ExperimentConfig(
                budget=0
            )

    def test_invalid_exploration_rate(self):
        with self.assertRaises(
            ValueError
        ):
            ExperimentConfig(
                exploration_rate=1.5
            )

    def test_invalid_memory_capacity(self):
        with self.assertRaises(
            ValueError
        ):
            ExperimentConfig(
                memory_capacity=0
            )


if __name__ == "__main__":
    unittest.main()
