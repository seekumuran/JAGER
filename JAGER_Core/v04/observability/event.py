from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class SecurityEvent:

    trace_id: str
    timestamp: str
    agent: str
    target: str
    operation: str
    resource: str
    decision: str
    reason: str
    risk: float
    experiment_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def create(
        cls,
        trace_id,
        agent,
        target,
        operation,
        resource,
        decision,
        reason,
        risk,
        experiment_id,
    ):

        return cls(
            trace_id=trace_id,
            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),

            agent=agent,
            target=target,
            operation=operation,
            resource=resource,
            decision=decision,
            reason=reason,
            risk=float(risk),
            experiment_id=experiment_id,
        )
