from typing import Dict, Any

from .decision import SecurityDecision


class SecurityPolicy:

    def __init__(
        self,
        max_payload_size=4096,
        max_resource_risk=0.8,
    ):
        self.max_payload_size = (
            max_payload_size
        )

        self.max_resource_risk = (
            max_resource_risk
        )

    def evaluate(
        self,
        action: Dict[str, Any],
    ) -> SecurityDecision:

        parameters = action.get(
            "parameters",
            {},
        )

        payload_size = len(
            str(parameters)
        )

        if payload_size > (
            self.max_payload_size
        ):
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    "Payload exceeds "
                    "configured limit"
                ),
                risk=1.0,
            )

        if parameters.get(
            "credential_access",
            False,
        ):
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    "Credential access "
                    "is prohibited"
                ),
                risk=1.0,
            )

        if parameters.get(
            "system_access",
            False,
        ):
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    "System access "
                    "is prohibited"
                ),
                risk=1.0,
            )

        if parameters.get(
            "network_exfiltration",
            False,
        ):
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    "Network exfiltration "
                    "is prohibited"
                ),
                risk=1.0,
            )

        operation = parameters.get(
            "operation"
        )

        if operation in {
            "execute_shell",
            "modify_system",
            "read_credentials",
        }:
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    f"Operation "
                    f"'{operation}' "
                    f"is prohibited"
                ),
                risk=1.0,
            )

        risk = self._estimate_risk(
            action
        )

        if risk > self.max_resource_risk:
            return SecurityDecision(
                allowed=False,
                action=action.get(
                    "type",
                    "unknown",
                ),
                reason=(
                    "Estimated action "
                    "risk is too high"
                ),
                risk=risk,
            )

        return SecurityDecision(
            allowed=True,
            action=action.get(
                "type",
                "unknown",
            ),
            reason="Action permitted",
            risk=risk,
        )

    @staticmethod
    def _estimate_risk(action):

        parameters = action.get(
            "parameters",
            {},
        )

        risk = 0.0

        if parameters.get(
            "high_resource_usage",
            False,
        ):
            risk += 0.6

        if parameters.get(
            "external_network",
            False,
        ):
            risk += 0.4

        if parameters.get(
            "privileged",
            False,
        ):
            risk += 0.5

        return min(
            1.0,
            risk,
        )
