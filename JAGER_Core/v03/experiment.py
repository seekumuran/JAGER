from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class AdaptiveExperiment:
    experiment_id: str
    run_id: str
    inputs: Dict[str, Any]
    telemetry: Dict[str, Any]
    status: str
    strategy: str
    hypothesis_id: Optional[str]
    discovery: bool
    confirmed: bool
    reward: float

    def to_dict(self):
        return asdict(self)
