class TargetRegistry:

    def __init__(self):
        self._targets = {}

    def register(
        self,
        name,
        target,
    ):
        if not name:
            raise ValueError(
                "Target name cannot be empty."
            )

        if target is None:
            raise ValueError(
                "Target cannot be None."
            )

        self._targets[name] = target

    def get(self, name):
        if name not in self._targets:
            raise KeyError(
                f"Unknown target: {name}"
            )

        return self._targets[name]

    def names(self):
        return sorted(
            self._targets.keys()
        )

    def remove(self, name):
        self._targets.pop(
            name,
            None,
        )

    def __contains__(self, name):
        return name in self._targets
