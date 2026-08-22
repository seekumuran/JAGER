class CandidateVerifier:

    def __init__(
        self,
        target,
        attempts=3,
    ):
        self.target = target
        self.attempts = max(
            1,
            attempts,
        )

    def verify(
        self,
        candidate,
    ):
        results = []

        for _ in range(
            self.attempts
        ):
            result = self.target.observe(
                **candidate.inputs
            )

            results.append(
                result["status"]
            )

        failures = sum(
            status == "FAILED"
            for status in results
        )

        confirmed = (
            failures == len(results)
        )

        candidate.record_verification(
            confirmed
        )

        return {
            "candidate_id":
                    candidate.candidate_id,
            "attempts":
                    len(results),
            "results":
                    results,
            "failures":
                    failures,
            "confirmed":
                    confirmed,
        }
