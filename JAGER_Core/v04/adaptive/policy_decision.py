from dataclasses import dataclass


@dataclass
class PolicyDecision:

    mode: str
    exploration_rate: float
    reason: str

    def to_dict(self):

        return {
            "mode": self.mode,
            "exploration_rate":
                self.exploration_rate,
            "reason": self.reason,
        }


class AdaptiveDecisionPolicy:

    def decide(
        self,
        exploration_rate: float,
        has_history: bool,
    ) -> PolicyDecision:

        if not has_history:

            return PolicyDecision(
                mode="exploration",
                exploration_rate=1.0,
                reason=(
                    "No prior experiment "
                    "history is available."
                ),
            )

        if exploration_rate >= 0.5:

            return PolicyDecision(
                mode="exploration",
                exploration_rate=(
                    exploration_rate
                ),
                reason=(
                    "Exploration rate favors "
                    "searching new candidates."
                ),
            )

        return PolicyDecision(
            mode="exploitation",
            exploration_rate=(
                exploration_rate
            ),
            reason=(
                "Existing candidate evidence "
                "supports exploitation."
            ),
        )
