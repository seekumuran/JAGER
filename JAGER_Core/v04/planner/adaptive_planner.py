from typing import Optional

from .candidate_generator import (
    CandidateGenerator,
)

from .planner import (
    ExperimentPlanner,
)

from .replanner import (
    Replanner,
)

from .goal import Goal


class AdaptivePlanner:

    def __init__(
        self,
        planner: Optional[
            ExperimentPlanner
        ] = None,
        replanner: Optional[
            Replanner
        ] = None,
    ):

        self.planner = (
            planner
            or ExperimentPlanner()
        )

        self.replanner = (
            replanner
            or Replanner()
        )

    def initial_plan(
        self,
        goal: Goal,
        previous_experiences=None,
    ):

        return self.planner.plan(
            goal=goal,
            previous_experiences=
                previous_experiences,
        )

    def update(
        self,
        goal: Goal,
        plan,
        observations=None,
        discoveries=None,
        experiences=None,
    ):

        return self.replanner.replan(
            goal=goal,
            candidates=plan[
                "candidates"
            ],
            observations=observations,
            discoveries=discoveries,
            experiences=experiences,
        )
