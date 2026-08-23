from dataclasses import replace
from typing import Any, Dict, List
import random

from .candidate import Candidate
from .candidate_id import CandidateID


class CandidateMutator:

    def __init__(
        self,
        seed: int = 42,
        numeric_step: float = 0.10,
    ):

        self.rng = random.Random(seed)
        self.numeric_step = float(
            numeric_step
        )

    def mutate(
        self,
        candidate: Candidate,
        bounds: Dict[str, tuple] | None = None,
    ) -> Candidate:

        parameters = dict(
            candidate.parameters
        )

        if not parameters:
            return self._new_candidate(
                candidate,
                parameters,
            )

        parameter = self.rng.choice(
            list(parameters.keys())
        )

        value = parameters[
            parameter
        ]

        if isinstance(value, bool):
            parameters[
                parameter
            ] = not value

        elif isinstance(
            value,
            int,
        ):
            parameters[
                parameter
            ] = self._mutate_int(
                parameter,
                value,
                bounds,
            )

        elif isinstance(
            value,
            float,
        ):
            parameters[
                parameter
            ] = self._mutate_float(
                parameter,
                value,
                bounds,
            )

        elif isinstance(
            value,
            str,
        ):
            parameters[
                parameter
            ] = self._mutate_string(
                value
            )

        return self._new_candidate(
            candidate,
            parameters,
        )

    def mutate_many(
        self,
        candidate: Candidate,
        count: int,
        bounds=None,
    ) -> List[Candidate]:

        if count < 0:
            raise ValueError(
                "count cannot be negative"
            )

        return [
            self.mutate(
                candidate,
                bounds,
            )
            for _ in range(count)
        ]

    def _mutate_int(
        self,
        name,
        value,
        bounds,
    ):

        step = max(
            1,
            int(
                abs(value)
                * self.numeric_step
            ),
        )

        result = value + self.rng.choice(
            [-step, step]
        )

        return self._clamp(
            name,
            result,
            bounds,
        )

    def _mutate_float(
        self,
        name,
        value,
        bounds,
    ):

        magnitude = max(
            0.01,
            abs(value)
            * self.numeric_step,
        )

        result = value + (
            self.rng.uniform(
                -magnitude,
                magnitude,
            )
        )

        return self._clamp(
            name,
            result,
            bounds,
        )

    def _mutate_string(
        self,
        value,
    ):

        return value

    @staticmethod
    def _clamp(
        name,
        value,
        bounds,
    ):

        if not bounds or name not in bounds:
            return value

        minimum, maximum = bounds[
            name
        ]

        return max(
            minimum,
            min(
                maximum,
                value,
            ),
        )

    @staticmethod
    def _new_candidate(
        parent,
        parameters,
    ):

        candidate_id = (
            CandidateID.generate(
                parent.target,
                parameters,
            )
        )

        return Candidate(
            candidate_id=candidate_id,
            target=parent.target,
            parameters=parameters,
            source="mutation",
            parent_id=parent.candidate_id,
        )
