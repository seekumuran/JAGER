from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ExperimentRecord:
    experiment_id: str
    trace_id: str
    action_id: str
    status: str
    allowed: bool
    reward: float
    novelty: float
    strategy: str
    inputs: Dict[str, Any]
    telemetry: Dict[str, Any]

    def to_dict(self):
        return asdict(self)
