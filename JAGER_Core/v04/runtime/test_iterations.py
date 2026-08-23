import unittest

from .iteration_context import (
    IterationContext,
)

from .iteration_manager import (
    IterationManager,
)

from .iteration_history import (
    IterationHistory,
)


class TestIterationContext(
    unittest.TestCase
):

    def test_recording(self):

        context = IterationContext(
            experiment_id="exp-001",
            iteration=1,
            target="mock",
            objective="test",
        )

        context.record_observation(
            {"value": 10}
        )

        context.record_action(
            {"action": "probe"}
        )

        context.record_discovery(
            {"pattern": "stable"}
        )

        context.update_state(
            {"score": 0.9}
        )

        self.assertEqual(
            len(
                context.observations
            ),
            1,
        )

        self.assertEqual(
            len(
                context.actions
            ),
            1,
        )

        self.assertEqual(
            len(
                context.discoveries
            ),
            1,
        )

        self.assertEqual(
            context.state["score"],
            0.9,
        )


class TestIterationHistory(
    unittest.TestCase
):

    def test_history(self):

        history = IterationHistory()

        context = IterationContext(
            experiment_id="exp-001",
            iteration=1,
            target="mock",
            objective="test",
        )

        history.add(context)

        self.assertEqual(
            history.count(),
            1,
        )

        self.assertIs(
            history.latest(),
            context,
        )

        self.assertIs(
            history.get(1),
            context,
        )


class TestIterationManager(
    unittest.TestCase
):

    def test_lifecycle(self):

        manager = IterationManager()

        context = manager.start(
            experiment_id="exp-001",
            iteration=1,
            target="mock",
            objective="test",
            state={
                "initial": True
            },
        )

        manager.complete(
            context,
            state={
                "finished": True
            },
        )

        self.assertEqual(
            context.metadata["status"],
            "completed",
        )

        self.assertTrue(
            context.state["finished"]
        )

        self.assertIs(
            manager.current(),
            context,
        )

    def test_failure(self):

        manager = IterationManager()

        context = manager.start(
            experiment_id="exp-002",
            iteration=1,
            target="mock",
            objective="test",
        )

        manager.fail(
            context,
            "execution failed",
        )

        self.assertEqual(
            context.metadata["status"],
            "failed",
        )

        self.assertEqual(
            context.errors[0],
            "execution failed",
        )


if __name__ == "__main__":
    unittest.main()
