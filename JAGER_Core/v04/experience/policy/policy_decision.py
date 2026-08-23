from dataclasses import dataclass
from typing import List


@dataclass
class PolicyDecision:

    allowed: bool
    decision: str
    policy_id: str
    matched_rules: List[str]
    reason: str

    def to_dict(self):

        return {
            "allowed":
                self.allowed,
            "decision":
                self.decision,
            "policy_id":
                self.policy_id,
            "matched_rules":
                list(self.matched_rules),
            "reason":
                self.reason,
        }
