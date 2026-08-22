class TargetObserver:

    def __init__(self, target):
        self.target = target

    def observe(self, **inputs):

        result = self.target.observe(
            **inputs
        )

        if not isinstance(result, dict):
            raise TypeError(
                "Target must return a dictionary."
            )

        if "status" not in result:
            raise ValueError(
                "Target observation "
                "must contain status."
            )

        if "telemetry" not in result:
            raise ValueError(
                "Target observation "
                "must contain telemetry."
            )

        return result
