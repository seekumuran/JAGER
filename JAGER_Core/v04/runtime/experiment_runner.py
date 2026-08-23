from typing import Any, Dict, Optional

from ..evidence.backbone import (
    ActionRecord,
    InstrumentedBackbone,
    PolicyEvaluation,
    TargetResponse,
)

from ..executor.executor import (
    ExperimentExecutor,
)

from ..executor.action import (
    Action,
)

from ..policy.policy_context import (
    PolicyContext,
)

from ..policy.policy_mediator import (
    PolicyMediator,
)

from .experiment import (
    Experiment,
)


class ExperimentRunner:

    def __init__(
        self,
        executor: ExperimentExecutor,
        policy: PolicyMediator,
        backbone: Optional[
            InstrumentedBackbone
        ] = None,
    ):

        self.executor = executor
        self.policy = policy
        self.backbone = (
            backbone
            or InstrumentedBackbone()
        )

    def run(
        self,
        experiment: Experiment,
        action_type: str,
        parameters: Optional[
            Dict[str, Any]
        ] = None,
        risk_level: str = "unknown",
    ):

        experiment.start()

        parameters = dict(
            parameters or {}
        )

        context = PolicyContext(
            experiment_id=(
                experiment.experiment_id
            ),
            target=experiment.target,
            action_type=action_type,
            parameters=parameters,
            risk_level=risk_level,
        )

        decision = self.policy.evaluate(
            context
        )

        policy_event = (
            self.backbone
            .record_policy_evaluation(
                experiment.experiment_id,
                PolicyEvaluation(
                    policy_id=
                        decision.policy_id,
                    decision=
                        decision.decision,
                    reason=
                        decision.reason,
                    allowed=
                        decision.allowed,
                ),
            )
        )

        decision_event = (
            self.backbone.record_decision(
                experiment.experiment_id,
                decision.decision,
                decision.reason,
                policy_event.event_id,
            )
        )

        if not decision.allowed:

            experiment.fail()

            return {
                "experiment":
                    experiment,
                "allowed": False,
                "decision":
                    decision,
                "policy_event":
                    policy_event,
                "decision_event":
                    decision_event,
                "action_event":
                    None,
                "response_event":
                    None,
            }

        action = (
            self.executor.create_action(
                target=experiment.target,
                action_type=action_type,
                parameters=parameters,
                metadata={
                    "experiment_id":
                        experiment.experiment_id,
                },
            )
        )

        action_event = (
            self.backbone.record_action(
                experiment.experiment_id,
                ActionRecord(
                    action_type=
                        action.action_type,
                    parameters=
                        action.parameters,
                    environment_snapshot_hash=
                        experiment.metadata.get(
                            "environment_snapshot_hash",
                            "unknown",
                        ),
                ),
                decision_event.event_id,
            )
        )

        result = self.executor.execute(
            action
        )

        response_event = (
            self.backbone
            .record_target_response(
                experiment.experiment_id,
                TargetResponse(
                    return_value=
                        result.output,
                    status=
                        result.status,
                    duration_ms=
                        result.duration_ms,
                ),
                action_event.event_id,
            )
        )

        if result.succeeded():

            experiment.complete()

        else:

            experiment.fail()

        return {
            "experiment":
                experiment,
            "allowed": True,
            "decision":
                decision,
            "action":
                action,
            "result":
                result,
            "policy_event":
                policy_event,
            "decision_event":
                decision_event,
            "action_event":
                action_event,
            "response_event":
                response_event,
        }
