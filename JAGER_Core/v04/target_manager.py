from .targets import TargetRegistry


class TargetManager:

    def __init__(self):
        self.registry = TargetRegistry()
        self.active_target = None

    def register(self, target):
        self.registry.register(target)

    def select(self, name):

        target = self.registry.get(name)

        self.active_target = target

        return target

    def current(self):

        if self.active_target is None:
            raise RuntimeError(
                "No target has been selected."
            )

        return self.active_target

    def observe(self, **inputs):

        return self.current().observe(
            **inputs
        )

    def available_targets(self):

        return self.registry.names()
