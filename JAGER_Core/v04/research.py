from collections import Counter


class ResearchAnalyzer:
    def __init__(self, hunter):
        self.hunter = hunter

    def status_counts(self):
        return Counter(
            item["observation"].status
            for item in self.hunter.experiments
        )

    def strategy_counts(self):
        return Counter(
            item["experience"].useful
            for item in self.hunter.experiments
        )

    def rewards(self):
        return [
            item["experience"].reward
            for item in self.hunter.experiments
        ]

    def total_reward(self):
        return sum(self.rewards())

    def mean_reward(self):
        values = self.rewards()

        if not values:
            return 0.0

        return self.total_reward() / len(values)

    def discovery_count(self):
        return len(
            self.hunter.failed_discoveries
        )

    def summary(self):
        return {
            "experiments": len(
                self.hunter.experiments
            ),
            "status_counts": dict(
                self.status_counts()
            ),
            "discoveries": self.discovery_count(),
            "total_reward": self.total_reward(),
            "mean_reward": self.mean_reward(),
            "memory_size": len(
                self.hunter.memory
            ),
            "event_count": len(
                self.hunter.logger.events
            ),
        }
