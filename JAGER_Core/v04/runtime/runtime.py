from typing import Any, Dict, Optional

from ..evidence.backbone import (
    InstrumentedBackbone,
)

from ..evidence.chain import (
    EvidenceChain,
)

from ..executor.executor import (
    ExperimentExecutor,
)

from ..policy.policy_mediator import (
    PolicyMediator,
)

from .experiment import (
    Experiment,
)

from .experiment_runner import (
    ExperimentRunner,
)


class JagerRuntime:

    def __init__(
        self,
        executor: ExperimentExecutor,
        policy: PolicyMediator,
        backbone: Optional[
            InstrumentedBackbone
        ] = None,
    ):

        self.backbone = (
            backbone
            or InstrumentedBackbone()
        )

        self.runner = ExperimentRunner(
            executor=executor,
            policy=policy,
            backbone=self.backbone,
        )

        self.experiments: Dict[
            str, Experiment
        ] = {}

    def create_experiment(
        self,
        target: str,
        hypothesis: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        experiment = Experiment.create(
            target=target,
            hypothesis=hypothesis,
            metadata=metadata,
        )

        self.experiments[
            experiment.experiment_id
        ] = experiment

        return experiment

    def run(
        self,
        experiment: Experiment,
        action_type: str,
        parameters=None,
        risk_level: str = "unknown",
    ):

        return self.runner.run(
            experiment=experiment,
            action_type=action_type,
            parameters=parameters,
            risk_level=risk_level,
        )

    def evidence(
        self,
        experiment_id: str,
    ):

        events = (
            self.backbone
            .experiment_events(
                experiment_id
            )
        )

        return EvidenceChain(
            events
        )

    def get_experiment(
        self,
        experiment_id: str,
    ):

        return self.experiments.get(
            experiment_id
        )

    def snapshot(self):

        return {
            "experiments": [
                experiment.to_dict()
                for experiment
                in self.experiments.values()
            ],
            "event_count":
                len(self.backbone.events),
        }
