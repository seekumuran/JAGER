#!/usr/bin/env python3
"""
viewer.py
---------
JAGER observability terminal viewer (first-hour MVP).

This tool DISPLAYS security decision events already made by JAGER's
enforcement path (Capability Manager, Policy Engine, Information-Flow
Controller, Resource Governor). It makes no authorization decisions itself
-- see the architectural constraint in the observability task brief and
SRS Section 5.1.

Usage
-----
    # View the bundled mock dataset (JSON array)
    python3 viewer.py --source ../mock_data/mock_events.json

    # View a JSONL file once
    python3 viewer.py --source ../mock_data/live_events.jsonl --format jsonl

    # Tail a JSONL file as new events are appended (future live JAGER use)
    python3 viewer.py --source ../mock_data/live_events.jsonl --format jsonl --follow

    # No file at all: use the tiny built-in synthetic fallback
    python3 viewer.py --mock

Only the Python standard library is used, per the "keep dependencies
minimal" constraint.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Iterable

from event_source import (
    EventSource,
    JsonFileEventSource,
    JsonlFileEventSource,
    MockEventSource,
    EventValidationError,
)

# ANSI colors. Fall back to plain text automatically if the terminal
# doesn't support them (see supports_color()).
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
DIM = "\033[2m"

DECISION_COLOR = {
    "ALLOW": GREEN,
    "DENY": RED,
    "MODIFY": YELLOW,
    "THROTTLE": MAGENTA,
    "TERMINATE": RED + BOLD,
}

DECISION_LABEL = {
    "ALLOW": "ALLOW",
    "DENY": "DENY ",
    "MODIFY": "MODIFY",
    "THROTTLE": "THROTTLE",
    "TERMINATE": "TERMINATE",
}


def supports_color() -> bool:
    return sys.stdout.isatty()


def format_event(event: Dict[str, Any], use_color: bool) -> str:
    decision = event.get("decision", "UNKNOWN")
    color = DECISION_COLOR.get(decision, "") if use_color else ""
    reset = RESET if use_color else ""
    bold = BOLD if use_color else ""
    dim = DIM if use_color else ""

    label = DECISION_LABEL.get(decision, decision)
    line_width = 62

    lines = []
    lines.append("-" * line_width)
    lines.append(f"{bold}Agent     :{reset} {event.get('agent_id', '?')}")
    lines.append(f"{bold}Operation :{reset} {event.get('operation', '?')}")
    lines.append(f"{bold}Resource  :{reset} {event.get('resource', '?')}")
    lines.append(f"{bold}Decision  :{reset} {color}{label}{reset}")
    lines.append(f"{bold}Reason    :{reset} {event.get('reason', '?')}")
    if event.get("reason_code"):
        lines.append(f"{bold}Reason Cd :{reset} {dim}{event['reason_code']}{reset}")
    lines.append(f"{bold}Trace ID  :{reset} {event.get('trace_id', '?')}")
    if event.get("parent_trace_id"):
        lines.append(f"{bold}Parent TR :{reset} {dim}{event['parent_trace_id']}{reset}")
    lines.append(f"{bold}Timestamp :{reset} {event.get('timestamp', '?')}")
    if event.get("component"):
        lines.append(f"{bold}Component :{reset} {dim}{event['component']}{reset}")
    if event.get("data_classification"):
        lines.append(f"{bold}Data Class:{reset} {dim}{event['data_classification']}{reset}")
    if event.get("latency_ms") is not None:
        lines.append(f"{bold}Latency   :{reset} {dim}{event['latency_ms']} ms{reset}")
    lines.append("-" * line_width)
    return "\n".join(lines)


def summarize(events: Iterable[Dict[str, Any]], use_color: bool) -> None:
    bold = BOLD if use_color else ""
    reset = RESET if use_color else ""
    counts: Dict[str, int] = {}
    total = 0
    for event in events:
        d = event.get("decision", "UNKNOWN")
        counts[d] = counts.get(d, 0) + 1
        total += 1
    print(f"\n{bold}Summary:{reset} {total} event(s) loaded")
    for decision in ["ALLOW", "DENY", "MODIFY", "THROTTLE", "TERMINATE"]:
        if decision in counts:
            color = DECISION_COLOR.get(decision, "") if use_color else ""
            print(f"  {color}{decision:<10}{reset}: {counts[decision]}")
    print()


def build_source(args: argparse.Namespace) -> EventSource:
    if args.mock:
        return MockEventSource()

    if args.source is None:
        print("No --source given and --mock not set; using built-in mock fallback.\n")
        return MockEventSource()

    path = Path(args.source)
    fmt = args.format
    if fmt == "auto":
        fmt = "jsonl" if path.suffix == ".jsonl" else "json"

    if fmt == "jsonl":
        return JsonlFileEventSource(path)
    return JsonFileEventSource(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="JAGER observability terminal viewer (displays security decision events)."
    )
    parser.add_argument(
        "--source",
        help="Path to a JSON (array) or JSONL (one event per line) event file.",
    )
    parser.add_argument(
        "--format",
        choices=["auto", "json", "jsonl"],
        default="auto",
        help="Input format. 'auto' infers from file extension (default).",
    )
    parser.add_argument(
        "--follow",
        action="store_true",
        help="Tail the source file for newly appended events (JSONL sources only). "
        "Models how a future live JAGER component would stream events in.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Ignore --source and use the tiny built-in synthetic fallback dataset.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors even on a color-capable terminal.",
    )
    args = parser.parse_args()

    use_color = supports_color() and not args.no_color

    try:
        source = build_source(args)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"{BOLD}JAGER Observability Viewer{RESET}")
    print(f"{DIM}(display-only; does not enforce or alter any security decision){RESET}\n")

    try:
        if args.follow:
            if not isinstance(source, JsonlFileEventSource):
                print(
                    "Error: --follow is only supported for JSONL sources "
                    "(use --format jsonl or a .jsonl file).",
                    file=sys.stderr,
                )
                return 1
            print(f"Following {args.source} for new events (Ctrl+C to stop)...\n")
            for event in source.follow():
                print(format_event(event, use_color))
        else:
            events = list(source.events())
            if not events:
                print("No events found in source.")
                return 0
            for event in events:
                print(format_event(event, use_color))
            summarize(events, use_color)
    except EventValidationError as e:
        print(f"Event validation error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopped following.")
        return 0
    except BrokenPipeError:
        # Downstream consumer (e.g. `| head`) closed early; not a real error.
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
