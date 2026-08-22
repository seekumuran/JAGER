from .metrics import Metrics


class ExperimentMetrics:

    def __init__(self):
        self.metrics = Metrics()

    def record_action(self):
        self.metrics.increment(
            "actions"
        )

    def record_normal(self):
        self.metrics.increment(
            "normal"
        )

    def record_degraded(self):
        self.metrics.increment(
            "degraded"
        )

    def record_failure(self):
        self.metrics.increment(
            "failures"
        )

    def record_discovery(self):
        self.metrics.increment(
            "discoveries"
        )

    def record_reward(self, reward):
        self.metrics.observe(
            "reward",
            reward,
        )

    def record_novelty(self, novelty):
        self.metrics.observe(
            "novelty",
            novelty,
        )

    def summary(self):
        return self.metrics.summary()
