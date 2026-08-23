from typing import Any, Dict

from .runtime_observer import (
    RuntimeObserver,
)


class RuntimeDiagnostics:

    def __init__(
        self,
        observer: RuntimeObserver,
    ):

        self.observer = observer

    def counters(self) -> Dict[str, Any]:

        return self.observer.metrics.snapshot()[
            "counters"
        ]

    def events(self):

        return [
            event.to_dict()
            for event
            in self.observer.events.history()
        ]

    def traces(self):

        return self.observer.tracer.snapshot()

    def report(self):

        metrics = (
            self.observer.metrics.snapshot()
        )

        return {
            "metrics": metrics,
            "event_count": len(
                self.observer.events.history()
            ),
            "trace_count": len(
                self.observer.tracer.spans()
            ),
            "events": self.events(),
            "traces": self.traces(),
        }
