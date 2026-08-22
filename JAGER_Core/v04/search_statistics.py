from collections import Counter


class SearchStatistics:

    def __init__(self):
        self.strategies = Counter()
        self.statuses = Counter()
        self.actions = 0

    def record(
        self,
        strategy,
        status,
    ):
        self.actions += 1
        self.strategies[strategy] += 1
        self.statuses[status] += 1

    def summary(self):
        return {
            "actions": self.actions,
            "strategies": dict(
                self.strategies
            ),
            "statuses": dict(
                self.statuses
            ),
        }
