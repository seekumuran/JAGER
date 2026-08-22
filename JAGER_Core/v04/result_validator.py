class ResultValidator:

    REQUIRED_KEYS = {
        "run_id",
        "seed",
        "budget",
        "experiments",
        "events",
        "discoveries",
    }

    def validate(self, result):
        missing = (
            self.REQUIRED_KEYS
            - set(result.keys())
        )

        if missing:
            raise ValueError(
                "Result is missing fields: "
                f"{sorted(missing)}"
            )

        if result["budget"] < 1:
            raise ValueError(
                "Budget must be positive."
            )

        if len(result["experiments"]) > result["budget"]:
            raise ValueError(
                "Experiment count exceeds budget."
            )

        return True
