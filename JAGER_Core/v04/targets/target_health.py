from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class HealthRecord:

    target: str
    available: bool
    latency_ms: float
    checked_at: str
    details: Dict[str, Any]


class TargetHealthMonitor:

    def __init__(self):

        self.records = {}

    def record(
        self,
        target: str,
        available: bool,
        latency_ms: float,
        details=None,
    ):

        record = HealthRecord(
            target=target,
            available=available,
            latency_ms=float(
                latency_ms
            ),
            checked_at=(
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            details=details or {},
        )

        self.records[target] = record

        return record

    def get(
        self,
        target: str,
    ):

        return self.records.get(
            target
        )

    def healthy(
        self,
        target: str,
    ) -> bool:

        record = self.get(target)

        return (
            record is not None
            and record.available
        )

    def snapshot(self):

        return {
            target: {
                "available":
                    record.available,
                "latency_ms":
                    record.latency_ms,
                "checked_at":
                    record.checked_at,
                "details":
                    record.details,
            }
            for target, record
            in self.records.items()
        }
