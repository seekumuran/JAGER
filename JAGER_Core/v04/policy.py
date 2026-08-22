from .models import Action, SecurityDecision


class SecurityPolicy:
    def evaluate(self, action: Action) -> SecurityDecision:
        risk = 0.0

        if action.operation == "probe":
            risk = 0.20

        elif action.operation == "stress":
            risk = 0.60

        elif action.operation == "execute":
            risk = 0.80

        if action.parameters.get("num_threads", 0) > 350:
            risk += 0.15

        if action.parameters.get("num_processes", 0) > 180:
            risk += 0.15

        if risk >= 0.85:
            return SecurityDecision(
                allowed=False,
                reason="RESOURCE_RISK",
                risk=min(risk, 1.0),
            )

        return SecurityDecision(
            allowed=True,
            reason="POLICY_ALLOWED",
            risk=min(risk, 1.0),
        )
