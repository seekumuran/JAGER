import unittest

from .recovery_policy import (
    RecoveryPolicy,
)

from .recovery_manager import (
    RecoveryManager,
)

from .recovery_context import (
    RecoveryContext,
)


class TestRecoveryPolicy(
    unittest.TestCase
):

    def test_retry(self):

        policy = RecoveryPolicy(
            max_retries=2
        )

        decision = policy.decide(
            attempt=0
        )

        self.assertTrue(
            decision.retry
        )

        self.assertEqual(
            decision.next_attempt,
            1,
        )

    def test_stop_after_limit(self):

        policy = RecoveryPolicy(
            max_retries=2
        )

        decision = policy.decide(
            attempt=2
        )

        self.assertFalse(
            decision.retry
        )


class TestRecoveryManager(
    unittest.TestCase
):

    def test_recovers(self):

        manager = RecoveryManager(
            RecoveryPolicy(
                max_retries=2
            )
        )

        attempts = []

        def operation(attempt):

            attempts.append(attempt)

            if attempt == 0:
                raise RuntimeError(
                    "temporary failure"
                )

            return "success"

        result = manager.execute(
            operation
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["result"],
            "success",
        )

        self.assertEqual(
            result["attempts"],
            2,
        )

    def test_exhausted(self):

        manager = RecoveryManager(
            RecoveryPolicy(
                max_retries=1
            )
        )

        def operation(attempt):

            raise RuntimeError(
                "permanent failure"
            )

        result = manager.execute(
            operation
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["attempts"],
            2,
        )


class TestRecoveryContext(
    unittest.TestCase
):

    def test_context(self):

        context = RecoveryContext(
            experiment_id="exp-001"
        )

        context.record_failure(
            "temporary failure"
        )

        context.record_recovery()

        data = context.to_dict()

        self.assertEqual(
            data["experiment_id"],
            "exp-001",
        )

        self.assertEqual(
            data["failure_count"],
            1,
        )

        self.assertTrue(
            data["recovered"]
        )


if __name__ == "__main__":
    unittest.main()
