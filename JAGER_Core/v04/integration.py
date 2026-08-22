from .config import JagerConfig
from .hunter import JagerHunter
from .target_registry import TargetRegistry


class JagerRuntime:

    def __init__(
        self,
        config=None,
        target_registry=None,
    ):
        self.config = (
            config or JagerConfig()
        )

        self.registry = (
            target_registry
            or TargetRegistry()
        )

        self.hunter = None

    def attach_target(
        self,
        name,
        target,
    ):
        self.registry.register(
            name,
            target,
        )

    def start(
        self,
        target_name,
    ):
        target = self.registry.get(
            target_name
        )

        self.hunter = JagerHunter(
            seed=self.config.seed,
            budget=self.config.budget,
            target=target,
            exploration_rate=(
                self.config.exploration_rate
            ),
            memory_capacity=(
                self.config.memory_capacity
            ),
        )

        return self.hunter.run()

    def status(self):
        if self.hunter is None:
            return {
                "running": False,
                "target_count": len(
                    self.registry.names()
                ),
            }

        return self.hunter.state()
