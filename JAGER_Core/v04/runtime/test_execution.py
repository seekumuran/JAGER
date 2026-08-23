import unittest

from .execution_manager import (
    ExecutionManager,
)


class TestExecutionManager(
    unittest.TestCase
):

    def test_successful_execution(self):

        manager = ExecutionManager()

        record = manager.begin(
            action={
                "type": "probe"
            },
            iteration=1,
            experiment_id="exp-001",
        )

        result = manager.complete(
            record,
            output={
                "score": 0.92
            },
            duration_ms=12.5,
        )

        self.assertTrue(
            result.success
        )

        self.assertEqual(
            result.status,
            "completed",
        )

        self.assertEqual(
            manager.history.count(),
            1,
        )

        self.assertEqual(
            manager.latest().status,
            "completed",
        )

    def test_failed_execution(self):

        manager = ExecutionManager()

        record = manager.begin(
            action="probe",
            iteration=2,
        )

        result = manager.fail(
            record,
            "target unavailable",
        )

        self.assertFalse(
            result.success
        )

        self.assertEqual(
            result.status,
            "failed",
        )

        self.assertEqual(
            len(
                manager.history.failed()
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
