from typing import Dict

from .base import Target


class TargetRegistry:

    def __init__(self):
        self._targets: Dict[
            str,
            Target,
        ] = {}

    def register(
        self,
        target: Target,
    ):

        if not isinstance(
            target,
            Target,
        ):
            raise TypeError(
                "Target must implement "
                "the Target interface."
            )

        self._targets[
            target.name
        ] = target

    def get(self, name: str):

        if name not in self._targets:
            raise KeyError(
                f"Unknown target: {name}"
            )

        return self._targets[name]

    def names(self):

        return sorted(
            self._targets.keys()
        )

    def __contains__(self, name):

        return name in self._targets
