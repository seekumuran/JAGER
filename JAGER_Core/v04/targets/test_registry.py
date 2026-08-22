import unittest

from .registry import TargetRegistry
from .linux_target import LinuxTarget


class TestTargetRegistry(
    unittest.TestCase
):

    def test_register_and_get(self):

        registry = TargetRegistry()

        target = LinuxTarget()

        registry.register(target)

        self.assertIn(
            "linux",
            registry,
        )

        self.assertIs(
            registry.get("linux"),
            target,
        )

    def test_names(self):

        registry = TargetRegistry()

        registry.register(
            LinuxTarget()
        )

        self.assertEqual(
            registry.names(),
            ["linux"],
        )

    def test_unknown_target(self):

        registry = TargetRegistry()

        with self.assertRaises(
            KeyError
        ):
            registry.get("missing")


if __name__ == "__main__":
    unittest.main()
