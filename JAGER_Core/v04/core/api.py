from typing import Any, Dict, Optional

from .facade import Jager
from .health_service import HealthService


class JagerAPI:

    def __init__(self, jager: Jager):

        self.jager = jager

        self.health = HealthService(
            jager
        )

    def start(self):

        return self.jager.start()

    def stop(self):

        return self.jager.stop()

    def create_experiment(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.jager.create_experiment(
            name=name,
            objective=objective,
            target=target,
            metadata=metadata,
        )

    def execute(
        self,
        experiment_id: str,
        iteration: int,
        action: Any,
    ):

        return self.jager.execute(
            experiment_id,
            iteration,
            action,
        )

    def complete(
        self,
        record,
        output: Any = None,
        duration_ms: Optional[
            float
        ] = None,
    ):

        return self.jager.complete(
            record,
            output,
            duration_ms,
        )

    def evaluate(
        self,
        experiment_id: str,
        iteration: int,
        score: Optional[float] = None,
        error: Optional[str] = None,
    ):

        return self.jager.evaluate(
            experiment_id,
            iteration,
            score,
            error,
        )

    def snapshot(self):

        return self.jager.snapshot()

    def health_status(self):

        return self.health.status()

    def diagnostics(self):

        return self.health.diagnostics_snapshot()

    def summary(self):

        return self.health.summary()
