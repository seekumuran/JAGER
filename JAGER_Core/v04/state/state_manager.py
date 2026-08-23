from typing import Any, Dict, Optional

from .runtime_state import (
    RuntimeState,
)

from .state_store import (
    StateStore,
)


class StateManager:

    def __init__(
        self,
        store: Optional[
            StateStore
        ] = None,
    ):

        self.store = (
            store or StateStore()
        )

    def begin(
        self,
        experiment_id: str,
    ):

        return self.store.mutate(
            lambda state:
                state.start_experiment(
                    experiment_id
                )
        )

    def complete(
        self,
        experiment_id: str,
    ):

        return self.store.mutate(
            lambda state:
                state.complete_experiment(
                    experiment_id
                )
        )

    def fail(
        self,
        experiment_id: str,
    ):

        return self.store.mutate(
            lambda state:
                state.fail_experiment(
                    experiment_id
                )
        )

    def discovery_found(self):

        return self.store.mutate(
            lambda state:
                state.record_discovery()
        )

    def experience_created(self):

        return self.store.mutate(
            lambda state:
                state.record_experience()
        )

    def event(
        self,
        event_type: str,
        data: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.store.mutate(
            lambda state:
                state.record_event(
                    event_type,
                    data,
                )
        )

    def snapshot(self):

        return self.store.snapshot()

    def reset(self):

        self.store.reset()
