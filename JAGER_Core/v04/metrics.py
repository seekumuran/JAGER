class Metrics:
    def __init__(self):
        self.values = {
            "experiments": 0,
            "allowed": 0,
            "denied": 0,
            "normal": 0,
            "degraded": 0,
            "failed": 0,
            "discoveries": 0,
        }

    def record_decision(self, allowed):
        key = "allowed" if allowed else "denied"
        self.values[key] += 1

    def record_status(self, status):
        self.values[status.lower()] += 1
        self.values["experiments"] += 1

        if status == "FAILED":
            self.values["discoveries"] += 1

    def snapshot(self):
        return dict(self.values)

    def discovery_rate(self):
        experiments = self.values["experiments"]

        if experiments == 0:
            return 0.0

        return self.values["discoveries"] / experiments
