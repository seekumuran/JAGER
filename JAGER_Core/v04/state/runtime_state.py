from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class RuntimeState:

    started_at: float = field(
        default_factory=time.time
    )

    active_experiment_id: Optional[str] = None

    iteration: int = 0

    status: str = "idle"

    experiments_completed: int = 0
    experiments_failed: int = 0

    discoveries_found: int = 0
    experiences_created: int = 0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    history: List[Dict[str, Any]] = field(
        default_factory=list
    )

    def start_experiment(
        self,
        experiment_id: str,
    ):

        self.active_experiment_id = (
            experiment_id
        )

        self.status = "running"

        self.iteration += 1

    def complete_experiment(
        self,
        experiment_id: str,
    ):

        if (
            self.active_experiment_id
            != experiment_id
        ):
            return

        self.experiments_completed += 1

        self.active_experiment_id = None

        self.status = "idle"

    def fail_experiment(
        self,
        experiment_id: str,
    ):

        if (
            self.active_experiment_id
            != experiment_id
        ):
            return

        self.experiments_failed += 1

        self.active_experiment_id = None

        self.status = "idle"

    def record_discovery(self):

        self.discoveries_found += 1

    def record_experience(self):

        self.experiences_created += 1

    def record_event(
        self,
        event_type: str,
        data: Optional[
            Dict[str, Any]
        ] = None,
    ):

        self.history.append(
            {
                "timestamp":
                    time.time(),
                "type":
                    event_type,
                "data":
                    dict(data or {}),
            }
        )

    def to_dict(self):

        return {
            "started_at":
                self.started_at,
            "active_experiment_id":
                self.active_experiment_id,
            "iteration":
                self.iteration,
            "status":
                self.status,
            "experiments_completed":
                self.experiments_completed,
            "experiments_failed":
                self.experiments_failed,
            "discoveries_found":
                self.discoveries_found,
            "experiences_created":
                self.experiences_created,
            "metadata":
                dict(self.metadata),
            "history":
                list(self.history),
        }
