from dataclasses import dataclass


@dataclass
class Decision:
    action_id: str
    allowed: bool
    reason: str
    risk: float
    confidence: float


class DecisionEngine:
    def decide(self, policy_decision, confidence=1.0):
        return Decision(
            action_id="",
            allowed=policy_decision.allowed,
            reason=policy_decision.reason,
            risk=policy_decision.risk,
            confidence=confidence,
        )
