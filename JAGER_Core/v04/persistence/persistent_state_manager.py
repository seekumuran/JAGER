from typing import Any, Dict, Optional

from ..state.runtime_state import (
    RuntimeState,
)

from .json_runtime_state_repository import (
    JsonRuntimeStateRepository,
)


class PersistentStateManager:

    def __init__(
        self,
        repository:
            JsonRuntimeStateRepository,
    ):

        self.repository = repository

        self.state = (
            repository.load()
            or RuntimeState()
        )

    def _save(self):

        self.repository.save(
            self.state
        )

    def begin(
        self,
        experiment_id: str,
    ):

        self.state.start_experiment(
            experiment_id
        )

        self._save()

        return self.state

    def complete(
        self,
        experiment_id: str,
    ):

        self.state.complete_experiment(
            experiment_id
        )

        self._save()

        return self.state

    def fail(
        self,
        experiment_id: str,
    ):

        self.state.fail_experiment(
            experiment_id
        )

        self._save()

        return self.state

    def discovery_found(self):

        self.state.record_discovery()

        self._save()

        return self.state

    def experience_created(self):

        self.state.record_experience()

        self._save()

        return self.state

    def event(
        self,
        event_type: str,
        data: Optional[
            Dict[str, Any]
        ] = None,
    ):

        self.state.record_event(
            event_type,
            data,
        )

        self._save()

        return self.state

    def snapshot(self):

        return self.state.to_dict()

    def reset(self):

        self.state = RuntimeState()

        self._save()
