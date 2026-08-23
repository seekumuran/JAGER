import unittest

from .config import JagerConfig

from .engine import JagerEngine

from .errors import (
    ConfigurationError,
)


class TestJagerConfig(
    unittest.TestCase
):

    def test_valid_config(self):

        config = JagerConfig(
            max_iterations=20,
            max_actions=200,
        )

        self.assertTrue(
            config.validate()
        )

    def test_invalid_config(self):

        config = JagerConfig(
            max_iterations=0
        )

        with self.assertRaises(
            ConfigurationError
        ):

            config.validate()

    def test_roundtrip(self):

        config = JagerConfig(
            name="test",
            environment="test",
            metadata={
                "owner": "jager"
            },
        )

        restored = JagerConfig.from_dict(
            config.to_dict()
        )

        self.assertEqual(
            restored.name,
            "test",
        )

        self.assertEqual(
            restored.metadata["owner"],
            "jager",
        )


class TestJagerEngine(
    unittest.TestCase
):

    def test_start_stop(self):

        engine = JagerEngine()

        self.assertFalse(
            engine.started
        )

        engine.start()

        self.assertTrue(
            engine.started
        )

        engine.stop()

        self.assertFalse(
            engine.started
        )

    def test_snapshot(self):

        engine = JagerEngine()

        snapshot = engine.snapshot()

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
