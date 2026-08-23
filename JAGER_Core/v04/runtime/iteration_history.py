from typing import List, Optional

from .iteration_context import (
    IterationContext,
)


class IterationHistory:

    def __init__(self):

        self._iterations: List[
            IterationContext
        ] = []

    def add(
        self,
        context: IterationContext,
    ):

        self._iterations.append(
            context
        )

    def get(
        self,
        iteration: int,
    ) -> Optional[
        IterationContext
    ]:

        for context in self._iterations:

            if context.iteration == iteration:
                return context

        return None

    def latest(
        self,
    ) -> Optional[
        IterationContext
    ]:

        if not self._iterations:
            return None

        return self._iterations[-1]

    def all(self):

        return list(
            self._iterations
        )

    def count(self):

        return len(
            self._iterations
        )

    def clear(self):

        self._iterations.clear()

    def to_dict(self):

        return [
            context.to_dict()
            for context
            in self._iterations
        ]
