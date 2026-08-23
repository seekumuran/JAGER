import unittest

from .budget_manager import (
    BudgetManager,
)

from .lifecycle import (
    RuntimeLifecycle,
)

from .runtime_controller import (
    RuntimeController,
)

from .termination import (
    TerminationController,
)


class TestLifecycle(
    unittest.TestCase
):

    def test_lifecycle(self):

        lifecycle = RuntimeLifecycle()

        self.assertEqual(
            lifecycle.status,
            "created",
        )

        lifecycle.start()

        self.assertEqual(
            lifecycle.status,
            "running",
        )

        lifecycle.complete()

        self.assertTrue(
            lifecycle.is_terminal()
        )


class TestTermination(
    unittest.TestCase
):

    def test_target_score(self):

        controller = TerminationController(
            target_score=0.9
        )

        decision = controller.evaluate(
            iteration=2,
            score=0.95,
        )

        self.assertTrue(
            decision.should_stop
        )

        self.assertEqual(
            decision.status,
            "completed",
        )

    def test_iteration_limit(self):

        controller = TerminationController(
            maximum_iterations=5
        )

        decision = controller.evaluate(
            iteration=5
        )

        self.assertTrue(
            decision.should_stop
        )


class TestRuntimeController(
    unittest.TestCase
):

    def test_runtime(self):

        controller = RuntimeController(
            termination=
                TerminationController(
                    maximum_iterations=2
                )
        )

        controller.start()

        controller.begin_iteration()

        controller.record_action()

        decision = controller.evaluate(
            iteration=1
        )

        self.assertFalse(
            decision.should_stop
        )

        controller.begin_iteration()

        decision = controller.evaluate(
            iteration=2
        )

        self.assertTrue(
            decision.should_stop
        )

        self.assertEqual(
            controller.lifecycle.status,
            "completed",
        )

    def test_failure(self):

        controller = RuntimeController()

        controller.start()

        controller.fail(
            "executor failure"
        )

        self.assertEqual(
            controller.lifecycle.status,
            "failed",
        )

        self.assertTrue(
            controller.lifecycle.is_terminal()
        )


if __name__ == "__main__":
    unittest.main()
