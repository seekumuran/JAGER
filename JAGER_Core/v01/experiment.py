from dataclasses import dataclass, asdict
from typing import Any, Dict
import json


@dataclass
class ExperimentRecord:
    experiment_id: str
    run_id: str
    seed: int
    inputs: Dict[str, Any]
    telemetry: Dict[str, Any]
    status: str
    discovery: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)
