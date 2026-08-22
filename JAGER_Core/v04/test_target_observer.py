import unittest

from .target_observer import (
    TargetObserver,
)


class FakeTarget:

    name = "fake"

    def observe(self, **inputs):

        return {
            "inputs": inputs,
            "telemetry": {
                "value": 10
            },
            "status": "NORMAL",
        }


class TestTargetObserver(
    unittest.TestCase
):

    def test_observe(self):

        observer = TargetObserver(
            FakeTarget()
        )

        result = observer.observe(
            test=1
        )

        self.assertEqual(
            result["status"],
            "NORMAL",
        )

        self.assertEqual(
            result["inputs"]["test"],
            1,
        )

    def test_invalid_target(self):

        class BadTarget:

            def observe(self, **inputs):
                return {}

        observer = TargetObserver(
            BadTarget()
        )

        with self.assertRaises(
            ValueError
        ):
            observer.observe()


if __name__ == "__main__":
    unittest.main()
