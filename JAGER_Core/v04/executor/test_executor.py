import unittest

from .action import Action
from .executor import (
    ExperimentExecutor,
)
from .mock_target import MockTarget
from .registry import TargetRegistry


class TestExecutor(
    unittest.TestCase
):

    def setUp(self):

        self.registry = (
            TargetRegistry()
        )

        self.target = MockTarget(
            "mock"
        )

        self.registry.register(
            self.target
        )

        self.executor = (
            ExperimentExecutor(
                self.registry
            )
        )

    def test_target_registration(self):

        self.assertTrue(
            self.registry.contains(
                "mock"
            )
        )

        self.assertEqual(
            self.registry.names(),
            ["mock"],
        )

    def test_create_action(self):

        action = (
            self.executor.create_action(
                target="mock",
                action_type="probe",
                parameters={
                    "load": 80
                },
            )
        )

        self.assertEqual(
            action.target,
            "mock",
        )

        self.assertEqual(
            action.action_type,
            "probe",
        )

        self.assertTrue(
            action.action_id
        )

    def test_execute(self):

        action = Action(
            action_id="action-1",
            action_type="probe",
            target="mock",
            parameters={
                "load": 80
            },
        )

        result = (
            self.executor.execute(
                action
            )
        )

        self.assertTrue(
            result.succeeded()
        )

        self.assertEqual(
            result.status,
            "success",
        )

        self.assertIsNotNone(
            result.output
        )

        self.assertGreaterEqual(
            result.duration_ms,
            0,
        )

    def test_observe(self):

        observation = (
            self.executor.observe(
                "mock"
            )
        )

        self.assertEqual(
            observation["target"],
            "mock",
        )

    def test_failed_action(self):

        action = Action(
            action_id="action-2",
            action_type="invalid",
            target="mock",
        )

        result = (
            self.executor.execute(
                action
            )
        )

        self.assertTrue(
            result.failed()
        )

        self.assertEqual(
            result.status,
            "error",
        )

        self.assertIsNotNone(
            result.error
        )

    def test_unknown_target(self):

        action = Action(
            action_id="action-3",
            action_type="probe",
            target="unknown",
        )

        with self.assertRaises(
            KeyError
        ):

            self.executor.execute(
                action
            )


if __name__ == "__main__":
    unittest.main()
