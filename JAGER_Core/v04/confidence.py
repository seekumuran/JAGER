class ConfidenceEstimator:

    def estimate(
        self,
        observations,
        failures,
    ):
        if observations <= 0:
            return 0.0

        consistency = (
            failures / observations
        )

        return min(
            1.0,
            0.5 + consistency * 0.5,
        )

    def confirmation_confidence(
        self,
        successful_reproductions,
        attempts,
    ):
        if attempts <= 0:
            return 0.0

        return successful_reproductions / attempts
