from .hunter import JagerHunter
from .config import JagerConfig
from .research import ResearchAnalyzer


class JagerAgent:
    def __init__(self, config=None):
        self.config = config or JagerConfig()

        self.hunter = JagerHunter(
            seed=self.config.seed,
            budget=self.config.budget,
        )

        self.analyzer = ResearchAnalyzer(
            self.hunter
        )

        self.running = False

    def start(self):
        self.running = True

        discoveries = self.hunter.run()

        self.running = False

        return discoveries

    def observe_state(self):
        return {
            "running": self.running,
            "run_id": self.hunter.run_id,
            "experiments": len(
                self.hunter.experiments
            ),
            "memory": len(
                self.hunter.memory
            ),
            "discoveries": len(
                self.hunter.failed_discoveries
            ),
            "events": len(
                self.hunter.logger.events
            ),
        }

    def report(self):
        return self.analyzer.summary()
