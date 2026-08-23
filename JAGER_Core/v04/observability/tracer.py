from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Dict, Iterator, List, Optional


@dataclass
class TraceSpan:

    name: str

    started_at: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    duration_ms: Optional[float] = None

    success: Optional[bool] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    error: Optional[str] = None

    def finish(
        self,
        success: bool,
        duration_ms: float,
        error: Optional[str] = None,
    ):

        self.success = success
        self.duration_ms = duration_ms
        self.error = error

    def to_dict(self):

        return {
            "name": self.name,
            "started_at": self.started_at,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "metadata": dict(self.metadata),
            "error": self.error,
        }


class RuntimeTracer:

    def __init__(self):

        self._spans: List[
            TraceSpan
        ] = []

    @contextmanager
    def span(
        self,
        name: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Iterator[TraceSpan]:

        trace = TraceSpan(
            name=name,
            metadata=dict(
                metadata or {}
            ),
        )

        started = perf_counter()

        try:

            yield trace

            trace.finish(
                success=True,
                duration_ms=(
                    perf_counter() - started
                ) * 1000.0,
            )

        except Exception as exc:

            trace.finish(
                success=False,
                duration_ms=(
                    perf_counter() - started
                ) * 1000.0,
                error=str(exc),
            )

            raise

        finally:

            self._spans.append(trace)

    def spans(self):

        return list(self._spans)

    def snapshot(self):

        return [
            span.to_dict()
            for span in self._spans
        ]

    def clear(self):

        self._spans.clear()
