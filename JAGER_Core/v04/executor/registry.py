from typing import Dict

from .target import Target


class TargetRegistry:

    def __init__(self):

        self._targets: Dict[
            str, Target
        ] = {}

    def register(
        self,
        target: Target,
    ):

        if target.name in self._targets:
            raise ValueError(
                f"Target already registered: "
                f"{target.name}"
            )

        self._targets[
            target.name
        ] = target

        return target

    def unregister(
        self,
        name: str,
    ):

        return self._targets.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ):

        target = self._targets.get(
            name
        )

        if target is None:
            raise KeyError(
                f"Unknown target: {name}"
            )

        return target

    def contains(
        self,
        name: str,
    ):

        return name in self._targets

    def names(self):

        return list(
            self._targets.keys()
        )

    def clear(self):

        self._targets.clear()
