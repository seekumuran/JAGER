import random
import uuid
from typing import Dict, Any, Optional

from BlackBox.blackbox_system import SimulatedSystem
from .experiment import ExperimentRecord


class BaselineHunter:
    """
    JÄGER v0.1:
    Deterministic seeded random exploration with no memory or learning.
    """

    def __init__(
        self,
        seed: int = 42,
        budget: int = 1000,
        run_id: Optional[str] = None,
    ):
        self.seed = seed
        self.budget = budget
        self.run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"

        self.rng = random.Random(seed)
        self.system = SimulatedSystem(seed=seed)

        self.experiments = []
        self.discoveries = []

    def generate_input(self) -> Dict[str, Any]:
        return {
            "cpu_load": self.rng.uniform(0, 100),
            "memory_load": self.rng.uniform(0, 100),
            "num_processes": self.rng.randint(0, 200),
            "num_threads": self.rng.randint(0, 400),
            "ipc_intensity": self.rng.uniform(0, 100),
        }

    def run_experiment(self, number: int) -> ExperimentRecord:
        inputs = self.generate_input()

        result = self.system.observe(**inputs)

        discovery = result["status"] == "FAILED"

        record = ExperimentRecord(
            experiment_id=f"exp-{number:06d}",
            run_id=self.run_id,
            seed=self.seed,
            inputs=result["inputs"],
            telemetry=result["telemetry"],
            status=result["status"],
            discovery=discovery,
        )

        self.experiments.append(record)

        if discovery:
            self.discoveries.append(record)

        return record

    def run(self) -> ExperimentRecord | None:
        for number in range(1, self.budget + 1):
            record = self.run_experiment(number)

            if record.discovery:
                return record

        return None
