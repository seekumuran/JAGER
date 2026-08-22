from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class Hypothesis:
    hypothesis_id: str
    description: str
    confidence: float
    source: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Candidate:
    candidate_id: str
    inputs: Dict[str, Any]
    score: float
    strategy: str
    hypothesis_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Discovery:
    discovery_id: str
    experiment_id: str
    inputs: Dict[str, Any]
    status: str
    confirmed: bool
    reproduction_attempts: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
