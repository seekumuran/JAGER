from typing import Any, Dict, Optional

from .config import JagerConfig
from .engine import JagerEngine
from .factory import JagerFactory
from .service import JagerService


class Jager:

    def __init__(
        self,
        config: Optional[
            JagerConfig
        ] = None,
    ):

        self.engine = JagerFactory.create(
            config
        )

        self.service = JagerService(
            self.engine
        )

    def start(self):

        return self.service.initialize()

    def create_experiment(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.service.create(
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

        return self.service.execute(
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

        return self.service.complete(
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

        return self.service.evaluate(
            experiment_id=experiment_id,
            iteration=iteration,
            score=score,
            error=error,
        )

    def stop(self):

        return self.service.shutdown()

    def snapshot(self):

        return self.service.snapshot()
