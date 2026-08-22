import time
import uuid
from typing import Dict, Any


class AISandbox:

    name = "ai_sandbox"

    def __init__(self, seed=42):
        self.seed = seed
        self.actions = []

    def execute(
        self,
        operation: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        action_id = (
            f"action-{uuid.uuid4().hex[:12]}"
        )

        started = time.perf_counter()

        allowed = self._policy_check(
            operation,
            payload,
        )

        if allowed:
            outcome = self._execute_safe(
                operation,
                payload,
            )
            decision = "ALLOW"
            reason = "Operation permitted"

        else:
            outcome = None
            decision = "DENY"
            reason = (
                "Operation violates "
                "sandbox policy"
            )

        latency_ms = (
            time.perf_counter() - started
        ) * 1000.0

        result = {
            "action_id": action_id,
            "operation": operation,
            "decision": decision,
            "reason": reason,
            "outcome": outcome,
            "telemetry": {
                "latency_ms": latency_ms,
                "payload_size": len(
                    str(payload)
                ),
            },
        }

        self.actions.append(result)

        return result

    def observe(self):

        return {
            "inputs": {},
            "telemetry": {
                "action_count": len(
                    self.actions
                ),
                "allowed_actions": sum(
                    action["decision"] == "ALLOW"
                    for action in self.actions
                ),
                "denied_actions": sum(
                    action["decision"] == "DENY"
                    for action in self.actions
                ),
            },
            "status": "NORMAL",
        }

    @staticmethod
    def _policy_check(
        operation,
        payload,
    ):

        safe_operations = {
            "read_context",
            "summarize",
            "classify",
            "generate",
            "inspect",
        }

        if operation not in safe_operations:
            return False

        if payload.get(
            "system_access",
            False,
        ):
            return False

        if payload.get(
            "credential_access",
            False,
        ):
            return False

        if payload.get(
            "network_exfiltration",
            False,
        ):
            return False

        return True

    @staticmethod
    def _execute_safe(
        operation,
        payload,
    ):

        if operation == "read_context":
            return {
                "type": "context",
                "size": len(
                    str(payload)
                ),
            }

        if operation == "summarize":
            return {
                "type": "summary",
                "status": "completed",
            }

        if operation == "classify":
            return {
                "type": "classification",
                "status": "completed",
            }

        if operation == "generate":
            return {
                "type": "generation",
                "status": "completed",
            }

        if operation == "inspect":
            return {
                "type": "inspection",
                "status": "completed",
            }

        return None
