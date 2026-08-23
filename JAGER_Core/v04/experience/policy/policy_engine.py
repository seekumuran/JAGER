from typing import Dict, List

from .policy_rule import PolicyRule
from .policy_decision import PolicyDecision


class PolicyEngine:

    def __init__(
        self,
        policy_id: str = "jager-policy-v1",
    ):

        self.policy_id = policy_id
        self._rules: List[
            PolicyRule
        ] = []

    def add_rule(
        self,
        rule: PolicyRule,
    ):

        self._rules.append(rule)

        self._rules.sort(
            key=lambda item:
                item.priority,
            reverse=True,
        )

        return rule

    def remove_rule(
        self,
        rule_id: str,
    ):

        before = len(self._rules)

        self._rules = [
            rule
            for rule in self._rules
            if rule.rule_id != rule_id
        ]

        return len(
            self._rules
        ) != before

    def rules(self):

        return list(self._rules)

    def evaluate(
        self,
        context: Dict[str, object],
    ) -> PolicyDecision:

        matched = []

        for rule in self._rules:

            if rule.matches(context):

                matched.append(
                    rule.rule_id
                )

                if rule.effect == "DENY":

                    return PolicyDecision(
                        allowed=False,
                        decision="DENY",
                        policy_id=(
                            self.policy_id
                        ),
                        matched_rules=matched,
                        reason=(
                            rule.description
                        ),
                    )

                return PolicyDecision(
                    allowed=True,
                    decision="ALLOW",
                    policy_id=(
                        self.policy_id
                    ),
                    matched_rules=matched,
                    reason=(
                        rule.description
                    ),
                )

        return PolicyDecision(
            allowed=False,
            decision="DENY",
            policy_id=self.policy_id,
            matched_rules=[],
            reason=(
                "No policy rule permitted "
                "the requested action."
            ),
        )
