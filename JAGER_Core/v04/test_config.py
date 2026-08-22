import unittest

from .config import JagerConfig
from .config_validator import validate_config
from .errors import ConfigurationError


class TestConfig(unittest.TestCase):

    def test_default_config(self):
        config = JagerConfig()

        self.assertTrue(
            validate_config(config)
        )

    def test_invalid_budget(self):
        config = JagerConfig(
            budget=0
        )

        with self.assertRaises(
            ConfigurationError
        ):
            validate_config(config)

    def test_invalid_exploration_rate(self):
        config = JagerConfig(
            exploration_rate=2.0
        )

        with self.assertRaises(
            ConfigurationError
        ):
            validate_config(config)

    def test_invalid_memory_capacity(self):
        config = JagerConfig(
            memory_capacity=0
        )

        with self.assertRaises(
            ConfigurationError
        ):
            validate_config(config)


if __name__ == "__main__":
    unittest.main()
