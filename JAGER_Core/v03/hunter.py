import random
import uuid

from BlackBox.blackbox_system import SimulatedSystem

from .candidate_generator import CandidateGenerator
from .discovery import DiscoveryManager
from .experience import Experience, ExperienceStore
from .hypothesis import HypothesisEngine
from .policy import AdaptivePolicy
from .reproduction import ReproductionEngine
from .reward import calculate_reward
from .experiment import AdaptiveExperiment


class AdaptiveHunter:
    def __init__(
        self,
        seed: int = 42,
        budget: int = 1000,
    ):
        self.seed = seed
        self.budget = budget

        self.rng = random.Random(seed)

        self.run_id = f"run-{uuid.uuid4().hex[:12]}"

        self.system = SimulatedSystem(seed=seed)

        self.policy = AdaptivePolicy()
        self.memory = ExperienceStore()
        self.hypotheses = HypothesisEngine()
        self.generator = CandidateGenerator(self.rng)
        self.discovery_manager = DiscoveryManager()
        self.reproduction = ReproductionEngine(self.system)

        self.experiments = []

    def select_candidate(self, candidates):
        return max(
            candidates,
            key=lambda candidate: candidate.score
            + self.rng.uniform(0, 0.25),
        )

    def run(self):
        for number in range(1, self.budget + 1):

            mode = self.policy.choose_mode(
                self.rng.random()
            )

            hypotheses = self.hypotheses.generate(
                self.memory
            )

            candidates = self.generator.generate(
                hypotheses=hypotheses,
                experiences=self.memory,
                count=10,
            )

            if mode == "EXPLORE":
                candidate = self.rng.choice(candidates)
            else:
                candidate = self.select_candidate(candidates)

            result = self.system.observe(
                **candidate.inputs
            )

            discovery = self.discovery_manager.evaluate(
                experiment_id=f"exp-{number:06d}",
                inputs=result["inputs"],
                status=result["status"],
            )

            confirmed = False
            reproduced = False

            if discovery:
                successes = self.reproduction.reproduce(
                    result["inputs"],
                    attempts=3,
                )

                discovery = self.discovery_manager.confirm(
                    discovery,
                    successes,
                )

                reproduced = successes >= 2
                confirmed = discovery.confirmed

            reward = calculate_reward(
                status=result["status"],
                discovery=discovery is not None,
                reproduced=reproduced,
            )

            usefulness = max(
                0.0,
                reward,
            )

            experience = Experience(
                experiment_id=f"exp-{number:06d}",
                inputs=result["inputs"],
                telemetry=result["telemetry"],
                status=result["status"],
                discovery=discovery is not None,
                reward=reward,
                usefulness=usefulness,
            )

            self.memory.add(experience)

            experiment = AdaptiveExperiment(
                experiment_id=f"exp-{number:06d}",
                run_id=self.run_id,
                inputs=result["inputs"],
                telemetry=result["telemetry"],
                status=result["status"],
                strategy=(
                    candidate.strategy
                    if mode == "EXPLOIT"
                    else "EXPLORATION"
                ),
                hypothesis_id=candidate.hypothesis_id,
                discovery=discovery is not None,
                confirmed=confirmed,
                reward=reward,
            )

            self.experiments.append(experiment)

            self.policy.update(
                discovered=discovery is not None
            )

            if confirmed:
                return discovery

        return None
