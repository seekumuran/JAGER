from typing import Optional

from ..planner.adaptive_planner import (
    AdaptivePlanner,
)

from ..planner.goal import Goal

from ..runtime.experiment import (
    Experiment,
)

from .jager_orchestrator import (
    JagerOrchestrator,
)


class AdaptiveLoop:

    def __init__(
        self,
        orchestrator:
            JagerOrchestrator,
        planner:
            Optional[AdaptivePlanner] = None,
    ):

        self.orchestrator = orchestrator

        self.planner = (
            planner
            or AdaptivePlanner()
        )

    def run(
        self,
        goal: Goal,
        maximum_iterations: int = 3,
    ):

        if maximum_iterations <= 0:

            raise ValueError(
                "maximum_iterations "
                "must be positive"
            )

        context = None
        plan = self.planner.initial_plan(
            goal
        )

        history = []

        for iteration in range(
            maximum_iterations
        ):

            candidate = plan.get(
                "best"
            )

            if candidate is None:

                break

            experiment = (
                Experiment.create(
                    target=goal.target,
                    hypothesis=
                        candidate.hypothesis,
                    metadata={
                        "iteration":
                            iteration,
                    },
                )
            )

            context, result = (
                self.orchestrator
                .execute_candidate(
                    experiment,
                    candidate,
                    risk_level=(
                        "low"
                        if candidate.risk
                        <= 0.25
                        else "medium"
                    ),
                )
            )

            history.append({
                "iteration":
                    iteration,
                "candidate":
                    candidate,
                "result":
                    result,
                "context":
                    context,
            })

            if result.status == "denied":

                break

            plan = self.planner.update(
                goal=goal,
                plan=plan,
                observations=
                    context.observations,
                discoveries=
                    context.discoveries,
                experiences=
                    context.experiences,
            )

        return {
            "goal": goal,
            "history": history,
            "final_plan": plan,
            "iterations":
                len(history),
        }
