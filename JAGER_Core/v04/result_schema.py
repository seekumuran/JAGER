from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class ObservationRecord:
    status: str
    telemetry: Dict[str, Any]
    inputs: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


@dataclass
class ExperimentRecord:
    experiment_id: str
    run_id: str
    sequence: int
    action: Dict[str, Any]
    observation: ObservationRecord
    reward: float
    novelty: float
    timestamp: float = field(
        default_factory=time.time
    )

    def to_dict(self):
        return asdict(self)


@dataclass
class RunSummary:
    run_id: str
    jager_version: str
    target: str
    seed: int
    budget: int

    experiments: int = 0
    candidates: int = 0
    verified: int = 0

    normal: int = 0
    degraded: int = 0
    failed: int = 0

    started_at: Optional[float] = None
    finished_at: Optional[float] = None

    def finalize(self):
        self.finished_at = time.time()

    def to_dict(self):
        return asdict(self)


@dataclass
class ExperimentRun:
    summary: RunSummary
    records: List[ExperimentRecord] = field(
        default_factory=list
    )

    def add(
        self,
        record: ExperimentRecord,
    ):
        self.records.append(record)

        self.summary.experiments += 1

        status = record.observation.status

        if status == "NORMAL":
            self.summary.normal += 1

        elif status == "DEGRADED":
            self.summary.degraded += 1

        elif status == "FAILED":
            self.summary.failed += 1

    def set_discoveries(
        self,
        candidates,
        verified,
    ):
        self.summary.candidates = candidates
        self.summary.verified = verified

    def finalize(self):
        self.summary.finalize()

    def to_dict(self):
        return {
            "summary":
                self.summary.to_dict(),
            "records": [
                record.to_dict()
                for record in self.records
            ],
        }
