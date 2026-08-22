from dataclasses import dataclass
from typing import Dict, Any
import time


@dataclass
class TelemetrySnapshot:

    target: str
    experiment_id: str
    timestamp: float
    status: str
    telemetry: Dict[str, Any]

    def to_dict(self):

        return {
            "target": self.target,
            "experiment_id":
                self.experiment_id,
            "timestamp":
                self.timestamp,
            "status":
                self.status,
            "telemetry":
                self.telemetry,
        }


class SnapshotStore:

    def __init__(
        self,
        max_snapshots: int = 1000,
    ):

        self.max_snapshots = int(
            max_snapshots
        )

        self.snapshots = []

    def add(
        self,
        target: str,
        experiment_id: str,
        status: str,
        telemetry: Dict[str, Any],
    ):

        snapshot = TelemetrySnapshot(
            target=target,
            experiment_id=experiment_id,
            timestamp=time.time(),
            status=status,
            telemetry=dict(telemetry),
        )

        self.snapshots.append(
            snapshot
        )

        if len(self.snapshots) > (
            self.max_snapshots
        ):

            self.snapshots = (
                self.snapshots[
                    -self.max_snapshots:
                ]
            )

        return snapshot

    def latest(
        self,
        target=None,
    ):

        if target is None:

            if not self.snapshots:
                return None

            return self.snapshots[-1]

        for snapshot in reversed(
            self.snapshots
        ):

            if snapshot.target == target:
                return snapshot

        return None

    def for_target(
        self,
        target: str,
    ):

        return [
            snapshot
            for snapshot in self.snapshots
            if snapshot.target == target
        ]

    def count(
        self,
        target=None,
    ):

        if target is None:
            return len(self.snapshots)

        return len(
            self.for_target(target)
        )

    def clear(self):

        self.snapshots.clear()
