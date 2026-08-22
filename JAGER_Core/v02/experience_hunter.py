import random
import uuid

from BlackBox.blackbox_system import SimulatedSystem

from .experience import Experience
from .memory import ExperienceMemory


class ExperienceHunter:
    """
    JÄGER v0.2.

    Uses persistent experience to bias future experiments.
    No LLM and no complex learning yet.
    """

    def __init__(self, seed=42, budget=1000):
        self.seed = seed
        self.budget = budget
        self.rng = random.Random(seed)

        self.run_id = f"run-{uuid.uuid4().hex[:12]}"
        self.system = SimulatedSystem(seed=seed)
        self.memory = ExperienceMemory()

        self.experiments = []
        self.discoveries = []

    def random_input(self):
        return {
            "cpu_load": self.rng.uniform(0, 100),
            "memory_load": self.rng.uniform(0, 100),
            "num_processes": self.rng.randint(0, 200),
            "num_threads": self.rng.randint(0, 400),
            "ipc_intensity": self.rng.uniform(0, 100),
        }

    def input_from_experience(self, experience):
        base = experience.inputs

        def perturb(value, amount, low, high):
            return max(low, min(high, value + self.rng.uniform(-amount, amount)))

        return {
            "cpu_load": perturb(base["cpu_load"], 10, 0, 100),
            "memory_load": perturb(base["memory_load"], 10, 0, 100),
            "num_processes": int(
                perturb(base["num_processes"], 20, 0, 200)
            ),
            "num_threads": int(
                perturb(base["num_threads"], 30, 0, 400)
            ),
            "ipc_intensity": perturb(
                base["ipc_intensity"], 10, 0, 100
            ),
        }

    def choose_input(self):
        experience = self.memory.retrieve()

        # Explore until useful experience exists.
        if experience is None:
            return self.random_input()

        # Exploit around the most useful previous experience.
        return self.input_from_experience(experience)

    def run(self):
        for number in range(1, self.budget + 1):

            inputs = self.choose_input()
            result = self.system.observe(**inputs)

            discovery = result["status"] == "FAILED"

            usefulness = 1.0 if discovery else 0.1

            experience = Experience(
                inputs=result["inputs"],
                telemetry=result["telemetry"],
                status=result["status"],
                discovery=discovery,
                usefulness=usefulness,
            )

            self.memory.add(experience)

            self.experiments.append(experience)

            if discovery:
                self.discoveries.append(experience)
                return experience

        return None
