import unittest

from .health import HealthChecker
from .jager import create


class TestHealth(
    unittest.TestCase
):

    def test_health(self):

        jager = create()

        health = HealthChecker(
            jager
        ).check()

        self.assertTrue(
            health.healthy
        )

        self.assertEqual(
            health.status,
            "healthy",
        )


if __name__ == "__main__":

    unittest.main()
