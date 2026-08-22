from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Experience:
    inputs: Dict[str, Any]
    telemetry: Dict[str, Any]
    status: str
    discovery: bool
    usefulness: float = 0.0

    def to_dict(self):
        return asdict(self)
