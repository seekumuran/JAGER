import tempfile
import unittest
from pathlib import Path

from .config import (
    JagerConfig,
)

from .config_loader import (
    ConfigLoader,
)

from .defaults import (
    default_config,
)


class TestConfig(
    unittest.TestCase
):

    def test_defaults(self):

        config = default_config()

        self.assertEqual(
            config.max_iterations,
            3,
        )

        self.assertEqual(
            config.maximum_risk,
            0.5,
        )

        self.assertFalse(
            config.allow_unknown_risk
        )

    def test_validation(self):

        config = JagerConfig(
            max_iterations=0
        )

        with self.assertRaises(
            ValueError
        ):

            config.validate()

    def test_invalid_risk(self):

        config = JagerConfig(
            maximum_risk=2.0
        )

        with self.assertRaises(
            ValueError
        ):

            config.validate()

    def test_dict_loading(self):

        loader = ConfigLoader()

        config = loader.load_dict(
            {
                "max_iterations": 5,
                "maximum_risk": 0.4,
            }
        )

        self.assertEqual(
            config.max_iterations,
            5,
        )

        self.assertEqual(
            config.maximum_risk,
            0.4,
        )

    def test_file_roundtrip(self):

        loader = ConfigLoader()

        config = default_config()

        with tempfile.TemporaryDirectory() as tmp:

            path = Path(tmp) / "jager.json"

            loader.save_file(
                config,
                str(path),
            )

            loaded = loader.load_file(
                str(path)
            )

            self.assertEqual(
                loaded.to_dict(),
                config.to_dict(),
            )


if __name__ == "__main__":
    unittest.main()
