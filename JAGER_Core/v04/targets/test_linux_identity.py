import unittest

from .linux_probe import (
    collect_system_identity,
)


class TestLinuxIdentity(
    unittest.TestCase
):

    def test_identity(self):

        identity = (
            collect_system_identity()
        )

        self.assertIn(
            "platform",
            identity,
        )

        self.assertIn(
            "architecture",
            identity,
        )

        self.assertIn(
            "python_version",
            identity,
        )


if __name__ == "__main__":
    unittest.main()
