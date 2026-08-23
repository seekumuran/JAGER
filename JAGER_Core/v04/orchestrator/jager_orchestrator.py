from typing import Any, Dict, Optional

from ..discovery.discovery_pipeline import (
    DiscoveryPipeline,
)

from ..experience.experience_manager import (
    ExperienceManager,
)

from ..experience.discovery_bridge import (
    DiscoveryExperienceBridge,
)

from ..planner.planner import (
    ExperimentPlanner,
)

from ..planner.goal import (
    Goal,
)

from ..runtime.experiment import (
    Experiment,
)

from ..runtime.experiment_runner import (
    ExperimentRunner,
)

from .execution_context import (
    ExecutionContext,
)

from .orchestration_result import (
    OrchestrationResult,
)


class JagerOrchestrator:

    def __init__(
        self,
        planner: ExperimentPlanner,
        runner: ExperimentRunner,
        discovery_pipeline:
            Optional[
                DiscoveryPipeline
            ] = None,
        experience_manager:
            Optional[
                ExperienceManager
            ] = None,
    ):

        self.planner = planner
        self.runner = runner

        self.discovery_pipeline = (
            discovery_pipeline
            or DiscoveryPipeline()
        )

        self.experience_manager = (
            experience_manager
            or ExperienceManager()
        )

        self.bridge = (
            DiscoveryExperienceBridge(
                self.experience_manager
            )
        )

    def create_context(
        self,
        experiment: Experiment,
    ):

        previous = (
            self.experience_manager
            .store
            .for_target(
                experiment.target
            )
        )

        return ExecutionContext(
            experiment_id=
                experiment.experiment_id,
            target=
                experiment.target,
            hypothesis=
                experiment.hypothesis,
            metadata=
                dict(experiment.metadata),
            previous_experiences=
                previous,
        )

    def plan(
        self,
        goal: Goal,
        context: Optional[
            ExecutionContext
        ] = None,
    ):

        experiences = None

        if context is not None:

            experiences = (
                context.previous_experiences
            )

        return self.planner.plan(
            goal=goal,
            previous_experiences=
                experiences,
        )

    def execute_candidate(
        self,
        experiment: Experiment,
        candidate,
        risk_level: str = "low",
    ):

        context = self.create_context(
            experiment
        )

        result = self.runner.run(
            experiment=experiment,
            action_type=
                candidate.action_type,
            parameters=
                candidate.parameters,
            risk_level=risk_level,
        )

        if not result.get("allowed"):

            return (
                context,
                OrchestrationResult(
                    status="denied",
                    experiment_id=
                        experiment.experiment_id,
                    reason=(
                        result[
                            "decision"
                        ].reason
                    ),
                ),
            )

        execution = result["result"]

        output = execution.output

        if isinstance(output, dict):

            observation = dict(output)

        else:

            observation = {
                "value": output,
                "status":
                    execution.status,
            }

        context.add_observation(
            observation
        )

        evidence = (
            self.runner.backbone
            .experiment_events(
                experiment.experiment_id
            )
        )

        from ..evidence.chain import (
            EvidenceChain,
        )

        chain = EvidenceChain(
            evidence
        )

        discovery = (
            self.discovery_pipeline.process(
                experiment_id=
                    experiment.experiment_id,
                target=
                    experiment.target,
                observation=
                    observation,
                evidence=chain,
                baseline=
                    context.baseline,
            )
        )

        experience = None

        if discovery is not None:

            context.add_discovery(
                discovery
            )

            experience = (
                self.bridge.promote(
                    discovery=
                        discovery,
                    hypothesis=
                        experiment.hypothesis,
                    action=
                        candidate.to_dict(),
                    outcome=
                        observation,
                )
            )

            context.add_experience(
                experience
            )

        status = (
            "success"
            if execution.succeeded()
            else "error"
        )

        return (
            context,
            OrchestrationResult(
                status=status,
                experiment_id=
                    experiment.experiment_id,
                action=
                    result.get("action"),
                execution=
                    execution,
                discovery=
                    discovery,
                experience=
                    experience,
                reason=(
                    "Experiment executed."
                ),
            ),
        )
