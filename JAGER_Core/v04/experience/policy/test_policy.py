import unittest

from .default_policy import (
    build_default_policy,
)

from .policy_context import (
    PolicyContext,
)

from .policy_engine import (
    PolicyEngine,
)

from .policy_rule import (
    PolicyRule,
)


class TestPolicyEngine(
    unittest.TestCase
):

    def test_allow_low_risk_probe(self):

        engine = build_default_policy()

        context = PolicyContext(
            experiment_id="exp-001",
            target="blackbox",
            action_type="probe",
            risk_level="low",
        )

        decision = engine.evaluate(
            context.to_dict()
        )

        self.assertTrue(
            decision.allowed
        )

        self.assertEqual(
            decision.decision,
            "ALLOW",
        )

    def test_deny_unknown_risk(self):

        engine = build_default_policy()

        context = PolicyContext(
            experiment_id="exp-002",
            target="blackbox",
            action_type="probe",
            risk_level="unknown",
        )

        decision = engine.evaluate(
            context.to_dict()
        )

        self.assertFalse(
            decision.allowed
        )

        self.assertEqual(
            decision.decision,
            "DENY",
        )

    def test_deny_destructive_action(self):

        engine = build_default_policy()

        context = PolicyContext(
            experiment_id="exp-003",
            target="blackbox",
            action_type="destructive",
            risk_level="high",
        )

        decision = engine.evaluate(
            context.to_dict()
        )

        self.assertFalse(
            decision.allowed
        )

    def test_custom_rule(self):

        engine = PolicyEngine()

        engine.add_rule(
            PolicyRule(
                rule_id="allow-test",
                description="Test rule",
                effect="ALLOW",
                priority=10,
                conditions={
                    "action_type": "test"
                },
            )
        )

        context = {
            "action_type": "test"
        }

        decision = engine.evaluate(
            context
        )

        self.assertTrue(
            decision.allowed
        )

    def test_no_matching_rule_denies(self):

        engine = PolicyEngine()

        decision = engine.evaluate(
            {
                "action_type":
                    "something_unknown"
            }
        )

        self.assertFalse(
            decision.allowed
        )

    def test_mediator(self):

        engine = build_default_policy()

        from .policy_mediator import (
            PolicyMediator,
        )

        mediator = PolicyMediator(
            engine
        )

        context = PolicyContext(
            experiment_id="exp-004",
            target="linux",
            action_type="observe",
        )

        self.assertTrue(
            mediator.authorize(context)
        )


if __name__ == "__main__":
    unittest.main()
