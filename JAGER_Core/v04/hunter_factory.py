from .action_generator import ActionGenerator


class HunterCandidateFactory:

    def __init__(
        self,
        target_name,
        seed=42,
        candidate_count=8,
    ):
        self.target_name = target_name
        self.generator = ActionGenerator(
            seed=seed
        )
        self.candidate_count = candidate_count

    def __call__(self):

        return [
            self.generator.generate(
                self.target_name
            )
            for _ in range(
                self.candidate_count
            )
        ]
