from .hunter import JagerHunter
from .config import JagerConfig


class JagerRuntime:
    def __init__(self, config=None):
        self.config = config or JagerConfig()

        self.hunter = JagerHunter(
            seed=self.config.seed,
            budget=self.config.budget,
        )

        self.started = False
        self.finished = False

    def start(self):
        self.started = True
        self.finished = False

        return self.hunter.run()

    def stop(self):
        self.finished = True

    def status(self):
        return {
            "started": self.started,
            "finished": self.finished,
            "run_id": self.hunter.run_id,
            "experiments": len(
                self.hunter.experiments
            ),
            "memory_entries": len(
                self.hunter.memory
            ),
            "discoveries": len(
                self.hunter.failed_discoveries
            ),
            "events": len(
                self.hunter.logger.events
            ),
        }
