class DiscoveryConfirmation:
    def __init__(self, target):
        self.target = target

    def confirm(
        self,
        inputs,
        attempts=3,
    ):
        results = []

        for _ in range(attempts):
            results.append(
                self.target.observe(
                    **inputs
                )
            )

        failures = sum(
            result["status"] == "FAILED"
            for result in results
        )

        return {
            "attempts": attempts,
            "failures": failures,
            "confirmed": failures >= 2,
            "results": results,
        }
