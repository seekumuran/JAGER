from collections import defaultdict


class Metrics:

    def __init__(self):
        self.counters = defaultdict(int)
        self.values = defaultdict(list)

    def increment(
        self,
        name,
        amount=1,
    ):
        self.counters[name] += amount

    def observe(
        self,
        name,
        value,
    ):
        self.values[name].append(
            float(value)
        )

    def get(self, name):
        return self.counters.get(
            name,
            0,
        )

    def average(self, name):
        values = self.values.get(
            name,
            [],
        )

        if not values:
            return 0.0

        return sum(values) / len(values)

    def summary(self):
        return {
            "counters": dict(
                self.counters
            ),
            "averages": {
                key: self.average(key)
                for key in self.values
            },
        }
