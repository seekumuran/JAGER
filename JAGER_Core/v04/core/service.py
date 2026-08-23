from typing import Any, Dict, Optional

from .engine import JagerEngine


class JagerService:

    def __init__(
        self,
        engine: JagerEngine,
    ):

        self.engine = engine

    def initialize(self):

        self.engine.start()

        return {
            "status": "started",
            "version":
                self.engine.config.version,
        }

    def create(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.engine.create_experiment(
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

        return self.engine.run_iteration(
            experiment_id=experiment_id,
            iteration=iteration,
            action=action,
        )

    def complete(
        self,
        record,
        output: Any = None,
        duration_ms: Optional[
            float
        ] = None,
    ):

        return self.engine.complete_execution(
            record=record,
            output=output,
            duration_ms=duration_ms,
        )

    def evaluate(
        self,
        experiment_id: str,
        iteration: int,
        score: Optional[float] = None,
        error: Optional[str] = None,
    ):

        return self.engine.evaluate(
            experiment_id=experiment_id,
            iteration=iteration,
            score=score,
            error=error,
        )

    def shutdown(self):

        self.engine.stop()

        return {
            "status": "stopped"
        }

    def snapshot(self):

        return self.engine.snapshot()
