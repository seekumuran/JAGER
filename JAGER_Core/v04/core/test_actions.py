import unittest

from .action import Action
from .action_authorizer import (
    ActionAuthorizer,
)
from .action_dispatcher import (
    ActionDispatcher,
)
from .policy import PolicyRule
from .policy_engine import PolicyEngine
from .target import Target
from .target_controller import (
    TargetController,
)


class TestActions(
    unittest.TestCase
):

    def _controller(self):

        policies = PolicyEngine()

        policies.add_rule(
            PolicyRule(
                name="risk-limit",
                maximum_risk=0.5,
            )
        )

        controller = TargetController(
            policies=policies
        )

        controller.register(
            Target(
                target_id="blackbox",
                name="JAGER Blackbox",
                kind="simulated",
            )
        )

        return controller

    def test_authorization(self):

        controller = self._controller()

        authorizer = ActionAuthorizer(
            controller
        )

        action = Action(
            action_type="probe",
            target_id="blackbox",
            risk=0.2,
        )

        result = authorizer.authorize(
            action
        )

        self.assertTrue(
            result["allowed"]
        )

    def test_risk_rejection(self):

        controller = self._controller()

        authorizer = ActionAuthorizer(
            controller
        )

        action = Action(
            action_type="probe",
            target_id="blackbox",
            risk=0.9,
        )

        result = authorizer.authorize(
            action
        )

        self.assertFalse(
            result["allowed"]
        )

    def test_dispatch(self):

        controller = self._controller()

        dispatcher = ActionDispatcher(
            ActionAuthorizer(
                controller
            )
        )

        dispatcher.register(
            "probe",
            lambda action: {
                "target":
                    action.target_id
            },
        )

        result = dispatcher.dispatch(
            Action(
                action_type="probe",
                target_id="blackbox",
                risk=0.1,
            )
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["output"]["target"],
            "blackbox",
        )


if __name__ == "__main__":

    unittest.main()
