from typing import Any, Dict, Optional

from .experiment_runtime import (
    ExperimentRuntime,
)

from .session_manager import (
    SessionManager,
)


class RuntimeSessionManager:

    def __init__(
        self,
        runtime: Optional[
            ExperimentRuntime
        ] = None,
        sessions: Optional[
            SessionManager
        ] = None,
    ):

        self.runtime = (
            runtime
            or ExperimentRuntime()
        )

        self.sessions = (
            sessions
            or SessionManager()
        )

    def create(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        experiment = self.runtime.create(
            name=name,
            objective=objective,
            target=target,
            metadata=metadata,
        )

        session = self.sessions.create(
            metadata={
                "experiment":
                    experiment.experiment_id,
            }
        )

        self.sessions.start(
            session.session_id,
            experiment.experiment_id,
        )

        self.runtime.start(
            experiment.experiment_id
        )

        return session, experiment

    def snapshot(self):

        return {
            "sessions":
                self.sessions.snapshot(),
            "runtime":
                self.runtime.snapshot(),
        }

    def close(
        self,
        session_id: str,
    ):

        return self.sessions.close(
            session_id
        )
