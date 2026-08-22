from .candidate_detector import (
    CandidateDetector,
)
from .verifier import (
    CandidateVerifier,
)


class DiscoveryPipeline:

    def __init__(
        self,
        hunter,
        target,
        verification_attempts=3,
    ):
        self.hunter = hunter
        self.target = target

        self.detector = (
            CandidateDetector()
        )

        self.verifier = CandidateVerifier(
            target,
            attempts=verification_attempts,
        )

        self.verification_results = []

    def process(
        self,
        experiment,
    ):
        candidate = (
            self.detector.inspect(
                experiment
            )
        )

        if candidate is None:
            return None

        verification = (
            self.verifier.verify(
                candidate
            )
        )

        self.verification_results.append(
            verification
        )

        return {
            "candidate":
                candidate,
            "verification":
                verification,
        }

    def discoveries(self):
        return (
            self.detector.store
            .verified()
        )

    def candidates(self):
        return (
            self.detector.store.all()
        )

    def statistics(self):

        candidates = (
            self.detector.store.all()
        )

        verified = (
            self.detector.store.verified()
        )

        return {
            "candidates":
                len(candidates),
            "verified":
                len(verified),
            "verification_rate":
                self.detector.store
                .verification_rate(),
            "verification_attempts":
                sum(
                    result["attempts"]
                    for result
                    in self.verification_results
                ),
        }
