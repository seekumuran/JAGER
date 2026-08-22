import unittest

from .target_manager import TargetManager
from .targets.linux_target import LinuxTarget


class TestTargetManager(unittest.TestCase):

    def test_target_selection(self):

        manager = TargetManager()

        target = LinuxTarget()

        manager.register(target)

        selected = manager.select("linux")

        self.assertIs(
            selected,
            target,
        )

        self.assertIs(
            manager.current(),
            target,
        )

    def test_available_targets(self):

        manager = TargetManager()

        manager.register(
            LinuxTarget()
        )

        self.assertEqual(
            manager.available_targets(),
            ["linux"],
        )

    def test_observe_without_target(self):

        manager = TargetManager()

        with self.assertRaises(
            RuntimeError
        ):
            manager.observe()


if __name__ == "__main__":
    unittest.main()
