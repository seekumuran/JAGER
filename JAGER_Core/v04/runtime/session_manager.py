from typing import Dict, List, Optional

from .session import RuntimeSession


class SessionManager:

    def __init__(self):

        self._sessions: Dict[
            str,
            RuntimeSession,
        ] = {}

    def create(
        self,
        metadata: Optional[Dict] = None,
    ):

        session = RuntimeSession(
            metadata=dict(
                metadata or {}
            )
        )

        self._sessions[
            session.session_id
        ] = session

        return session

    def start(
        self,
        session_id: str,
        experiment_id: str,
    ):

        session = self.require(
            session_id
        )

        session.start(
            experiment_id
        )

        return session

    def pause(
        self,
        session_id: str,
    ):

        session = self.require(
            session_id
        )

        session.pause()

        return session

    def resume(
        self,
        session_id: str,
    ):

        session = self.require(
            session_id
        )

        session.resume()

        return session

    def close(
        self,
        session_id: str,
    ):

        session = self.require(
            session_id
        )

        session.close()

        return session

    def get(
        self,
        session_id: str,
    ) -> Optional[
        RuntimeSession
    ]:

        return self._sessions.get(
            session_id
        )

    def require(
        self,
        session_id: str,
    ) -> RuntimeSession:

        session = self.get(
            session_id
        )

        if session is None:

            raise KeyError(
                f"unknown session: "
                f"{session_id}"
            )

        return session

    def active(self):

        return [
            session
            for session
            in self._sessions.values()
            if session.is_active()
        ]

    def all(self) -> List[
        RuntimeSession
    ]:

        return list(
            self._sessions.values()
        )

    def snapshot(self):

        return [
            session.snapshot()
            for session
            in self._sessions.values()
        ]
