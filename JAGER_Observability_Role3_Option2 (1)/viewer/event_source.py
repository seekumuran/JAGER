"""
event_source.py
----------------
Event ingestion layer for the JAGER observability viewer.

This module defines a small abstraction (EventSource) so the viewer never
depends on *how* events arrive. Today, events come from static JSON files
or synthetic mock data. Later, a real JAGER component (Provenance Engine,
Policy Engine, etc.) can emit newline-delimited JSON events and be read by
JsonlFileEventSource in --follow mode, or a future network/queue-based
source can implement the same interface without any change to viewer.py.

    mock_events.json / live_events.jsonl
                |
                v
        EventSource implementation
                |
                v
        viewer.py (display only)

IMPORTANT: This module and the viewer are NOT part of JAGER's enforcement
path. They only read and display events that some other component already
decided and recorded. See SRS Section 5.1 / 10.2 and the architectural
constraint in the observability task brief: the viewer must never be
responsible for authorization.
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, List, Dict, Any


REQUIRED_FIELDS = [
    "timestamp",
    "event_type",
    "trace_id",
    "agent_id",
    "operation",
    "resource",
    "decision",
    "reason",
]

VALID_DECISIONS = {"ALLOW", "DENY", "MODIFY", "THROTTLE", "TERMINATE"}


class EventValidationError(ValueError):
    """Raised when an event is missing required fields or has an invalid decision."""


def validate_event(event: Dict[str, Any], source_label: str = "") -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in event]
    if missing:
        raise EventValidationError(
            f"Event from {source_label or 'unknown source'} is missing required "
            f"field(s): {', '.join(missing)}. Event: {event}"
        )
    if event["decision"] not in VALID_DECISIONS:
        raise EventValidationError(
            f"Event {event.get('trace_id')} has invalid decision "
            f"'{event['decision']}'. Must be one of {sorted(VALID_DECISIONS)}."
        )


class EventSource(ABC):
    """Abstract base for anything that can supply JAGER observability events."""

    @abstractmethod
    def events(self) -> Iterator[Dict[str, Any]]:
        """Yield validated event dicts, in order."""
        raise NotImplementedError

    def follow(self) -> Iterator[Dict[str, Any]]:
        """
        Optional: yield events as they arrive, blocking/polling as needed.
        Default implementation just replays events() once and stops; sources
        that support real tailing (e.g. JsonlFileEventSource) override this.
        """
        yield from self.events()


class JsonFileEventSource(EventSource):
    """Reads a single JSON file containing a top-level array of events."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def events(self) -> Iterator[Dict[str, Any]]:
        if not self.path.exists():
            raise FileNotFoundError(f"Event file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise EventValidationError(
                f"{self.path} must contain a top-level JSON array of events."
            )
        for i, event in enumerate(data):
            validate_event(event, source_label=f"{self.path}[{i}]")
            yield event


class JsonlFileEventSource(EventSource):
    """
    Reads newline-delimited JSON events, one event per line.
    This is the format future real JAGER components should emit, since it
    can be appended to safely while being tailed (--follow).
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _parse_line(self, line: str, line_no: int) -> Dict[str, Any] | None:
        line = line.strip()
        if not line:
            return None
        event = json.loads(line)
        validate_event(event, source_label=f"{self.path}:{line_no}")
        return event

    def events(self) -> Iterator[Dict[str, Any]]:
        if not self.path.exists():
            raise FileNotFoundError(f"Event file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                event = self._parse_line(line, line_no)
                if event is not None:
                    yield event

    def follow(self, poll_interval: float = 0.5) -> Iterator[Dict[str, Any]]:
        """
        Replay existing lines, then keep polling for newly appended lines,
        similar to `tail -f`. This models how a live JAGER component would
        stream events into the viewer.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Event file not found: {self.path}")
        with open(self.path, "r", encoding="utf-8") as f:
            line_no = 0
            while True:
                line = f.readline()
                if line:
                    line_no += 1
                    event = self._parse_line(line, line_no)
                    if event is not None:
                        yield event
                else:
                    time.sleep(poll_interval)


class MockEventSource(EventSource):
    """
    In-memory synthetic event source. Useful for tests or environments
    where no event file is available at all. Wraps a plain Python list of
    event dicts so it satisfies the same EventSource interface as the
    file-backed sources.
    """

    def __init__(self, events: List[Dict[str, Any]] | None = None):
        self._events = events if events is not None else _DEFAULT_MOCK_EVENTS

    def events(self) -> Iterator[Dict[str, Any]]:
        for i, event in enumerate(self._events):
            validate_event(event, source_label=f"MockEventSource[{i}]")
            yield event


# A tiny built-in fallback dataset so the viewer can run even with zero
# files present. The primary demo dataset lives in mock_data/mock_events.json.
_DEFAULT_MOCK_EVENTS: List[Dict[str, Any]] = [
    {
        "timestamp": "2026-08-22T09:00:00.000Z",
        "event_type": "security_decision",
        "trace_id": "trc-00000001",
        "agent_id": "Researcher-01",
        "operation": "AGGREGATE",
        "resource": "sales",
        "decision": "ALLOW",
        "reason": "Built-in fallback event: capability and policy match.",
        "reason_code": "CAPABILITY_AND_POLICY_MATCH",
    },
    {
        "timestamp": "2026-08-22T09:00:05.000Z",
        "event_type": "security_decision",
        "trace_id": "trc-00000002",
        "agent_id": "Researcher-01",
        "operation": "READ",
        "resource": "customer_pii.email",
        "decision": "DENY",
        "reason": "Built-in fallback event: missing capability.",
        "reason_code": "MISSING_CAPABILITY",
    },
]
