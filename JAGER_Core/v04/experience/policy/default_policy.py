from .policy_engine import PolicyEngine
from .policy_rule import PolicyRule


def build_default_policy() -> PolicyEngine:

    engine = PolicyEngine(
        policy_id="jager-default-v1"
    )

    engine.add_rule(
        PolicyRule(
            rule_id="deny-unknown-risk",
            description=(
                "Actions with unknown risk "
                "are denied by default."
            ),
            effect="DENY",
            priority=100,
            conditions={
                "risk_level": "unknown"
            },
        )
    )

    engine.add_rule(
        PolicyRule(
            rule_id="deny-destructive-actions",
            description=(
                "Destructive actions require "
                "an explicit policy."
            ),
            effect="DENY",
            priority=90,
            conditions={
                "action_type": "destructive"
            },
        )
    )

    engine.add_rule(
        PolicyRule(
            rule_id="allow-low-risk-probes",
            description=(
                "Low-risk probes are permitted "
                "for controlled experiments."
            ),
            effect="ALLOW",
            priority=50,
            conditions={
                "action_type": "probe",
                "risk_level": "low",
            },
        )
    )

    engine.add_rule(
        PolicyRule(
            rule_id="allow-observation",
            description=(
                "Passive observation is permitted."
            ),
            effect="ALLOW",
            priority=40,
            conditions={
                "action_type": "observe",
            },
        )
    )

    return engine
