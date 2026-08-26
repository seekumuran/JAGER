import unittest

from .policy import PolicyRule
from .policy_engine import PolicyEngine
from .target import (
    Target,
    TargetRegistry,
)


class TestPolicy(
    unittest.TestCase
):

    def test_blocked_action(self):

        engine = PolicyEngine()

        engine.add_rule(
            PolicyRule(
                name="block-delete",
                blocked_actions=[
                    "delete"
                ],
            )
        )

        decision = engine.evaluate(
            {
                "type": "delete"
            }
        )

        self.assertFalse(
            decision.allowed
        )

    def test_risk_limit(self):

        engine = PolicyEngine(
            [
                PolicyRule(
                    name="risk-limit",
                    maximum_risk=0.5,
                )
            ]
        )

        decision = engine.evaluate(
            {
                "type": "probe"
            },
            risk=0.8,
        )

        self.assertFalse(
            decision.allowed
        )

    def test_allowed(self):

        engine = PolicyEngine()

        decision = engine.evaluate(
            {
                "type": "probe"
            }
        )

        self.assertTrue(
            decision.allowed
        )


class TestTargets(
    unittest.TestCase
):

    def test_registry(self):

        registry = TargetRegistry()

        target = Target(
            target_id="target-1",
            name="blackbox",
            kind="simulated",
        )

        registry.register(
            target
        )

        self.assertIs(
            registry.get("target-1"),
            target,
        )

        target.deactivate()

        self.assertEqual(
            len(registry.active()),
            0,
        )


if __name__ == "__main__":

    unittest.main()
