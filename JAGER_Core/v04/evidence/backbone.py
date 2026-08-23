from dataclasses import dataclass
from typing import Any, Dict, Optional

from .event import EvidenceEvent


@dataclass
class PolicyEvaluation:

    policy_id: str
    decision: str
    reason: str
    allowed: bool

    def to_dict(self):

        return {
            "policy_id": self.policy_id,
            "decision": self.decision,
            "reason": self.reason,
            "allowed": self.allowed,
        }


@dataclass
class ActionRecord:

    action_type: str
    parameters: Dict[str, Any]
    environment_snapshot_hash: str

    def to_dict(self):

        return {
            "action_type":
                self.action_type,
            "parameters":
                dict(self.parameters),
            "environment_snapshot_hash":
                self.environment_snapshot_hash,
        }


@dataclass
class TargetResponse:

    return_value: Any
    status: str
    duration_ms: float

    def to_dict(self):

        return {
            "return_value":
                self.return_value,
            "status":
                self.status,
            "duration_ms":
                self.duration_ms,
        }


class InstrumentedBackbone:

    POLICY_EVALUATION = (
        "policy_evaluation"
    )

    DECISION = "decision"

    ACTION = "action"

    TARGET_RESPONSE = (
        "target_response"
    )

    def __init__(self):

        self.events = []

    def record_policy_evaluation(
        self,
        experiment_id: str,
        evaluation: PolicyEvaluation,
    ):

        event = EvidenceEvent.create(
            event_type=(
                self.POLICY_EVALUATION
            ),
            experiment_id=experiment_id,
            payload=evaluation.to_dict(),
            source="policy_mediation",
        )

        self.events.append(event)

        return event

    def record_decision(
        self,
        experiment_id: str,
        decision: str,
        reason: str,
        parent_event_id: Optional[
            str
        ] = None,
    ):

        event = EvidenceEvent.create(
            event_type=self.DECISION,
            experiment_id=experiment_id,
            payload={
                "decision": decision,
                "reason": reason,
            },
            source="policy_mediation",
            parent_event_id=(
                parent_event_id
            ),
        )

        self.events.append(event)

        return event

    def record_action(
        self,
        experiment_id: str,
        action: ActionRecord,
        parent_event_id: Optional[
            str
        ] = None,
    ):

        event = EvidenceEvent.create(
            event_type=self.ACTION,
            experiment_id=experiment_id,
            payload=action.to_dict(),
            source="executor",
            parent_event_id=(
                parent_event_id
            ),
        )

        self.events.append(event)

        return event

    def record_target_response(
        self,
        experiment_id: str,
        response: TargetResponse,
        parent_event_id: Optional[
            str
        ] = None,
    ):

        event = EvidenceEvent.create(
            event_type=(
                self.TARGET_RESPONSE
            ),
            experiment_id=experiment_id,
            payload=response.to_dict(),
            source="target",
            parent_event_id=(
                parent_event_id
            ),
        )

        self.events.append(event)

        return event

    def experiment_events(
        self,
        experiment_id: str,
    ):

        return [
            event
            for event in self.events
            if event.experiment_id
            == experiment_id
        ]

    def clear(self):

        self.events.clear()
