# JÄGER Observability & Runtime Intelligence — First-Hour MVP

**Role owned:** Role 3 — Observability & Runtime Intelligence
**Status:** Working first-hour MVP. Displays JAGER security decision events; does **not** make security decisions itself.

## 1. What this component does

JAGER's enforcement path (Capability Manager → Policy Engine → Information-Flow
Controller → Resource Governor → Adapter → Provenance Engine, per SRS Section 5.1)
produces a decision — `ALLOW`, `DENY`, `MODIFY`, `THROTTLE`, or `TERMINATE` — for
every protected operation an agent attempts. This component:

1. Defines a simple, structured JSON event format for those decisions.
2. Ships a synthetic mock dataset that exercises every decision type.
3. Provides a terminal viewer that loads events from a file and displays them
   with the fields required for audit: agent, operation, resource, decision,
   reason, and trace ID — with ALLOW/DENY made visually obvious via color.
4. Defines a small `EventSource` abstraction so a real JAGER component can be
   plugged in later (e.g. a JSONL log tailed with `--follow`) without
   rewriting the viewer.

**Architectural boundary (important):** this component is read-only. It
records/displays decisions that JAGER's enforcement layer already made. It
never authorizes, blocks, or modifies a request. See Section 8 below.

## 2. Repository layout

```
jager-observability/
├── schema/
│   └── event_schema.json      # JSON Schema for a JAGER observability event
├── mock_data/
│   ├── mock_events.json       # 10 synthetic events (JSON array) — main demo dataset
│   └── live_events.jsonl      # 2 synthetic events (JSONL) — demonstrates --follow
├── viewer/
│   ├── event_source.py        # EventSource abstraction + Json/Jsonl/Mock implementations
│   └── viewer.py              # Terminal viewer (entry point)
└── README.md                  # This file
```

## 3. Event schema

Every event is a flat JSON object. Required fields:

| Field | Description |
|---|---|
| `timestamp` | UTC ISO-8601 time the enforcement path recorded the event |
| `event_type` | Event category, e.g. `security_decision` |
| `trace_id` | Unique ID for the protected operation (NFR-04) |
| `agent_id` | Requesting agent's identity (FR-01) |
| `operation` | Verb requested, e.g. `READ`, `AGGREGATE`, `EXPORT` |
| `resource` | Resource or resource pattern targeted |
| `decision` | One of `ALLOW`, `DENY`, `MODIFY`, `THROTTLE`, `TERMINATE` (SRS §10.2) |
| `reason` | Human-readable explanation (FR-21, NFR-08) |

Optional fields used in the mock data and supported by the viewer:
`reason_code`, `policy_version`, `capability`, `data_classification`,
`latency_ms`, `component`, `parent_trace_id`, `metadata`.

Full machine-readable definition: [`schema/event_schema.json`](schema/event_schema.json).

Example:

```json
{
  "timestamp": "2026-08-22T09:00:09.771Z",
  "event_type": "security_decision",
  "trace_id": "trc-3c4d5e6f",
  "agent_id": "Researcher-01",
  "operation": "READ",
  "resource": "customer_pii.email",
  "decision": "DENY",
  "reason": "Agent does not hold READ:customer_pii capability; default-deny applies.",
  "reason_code": "MISSING_CAPABILITY",
  "policy_version": "1.0.0",
  "capability": "READ:customer_pii",
  "data_classification": "PII",
  "latency_ms": 3.1,
  "component": "capability_manager"
}
```

## 4. How to run the viewer

Requires Python 3.10+ (standard library only — no dependencies to install).

```bash
cd jager-observability

# View the bundled 10-event mock dataset
python3 viewer/viewer.py --source mock_data/mock_events.json

# View a JSONL file once
python3 viewer/viewer.py --source mock_data/live_events.jsonl --format jsonl

# Tail a JSONL file live, as a future JAGER component would append to it
python3 viewer/viewer.py --source mock_data/live_events.jsonl --format jsonl --follow

# No file at all — tiny built-in synthetic fallback
python3 viewer/viewer.py --mock

# Disable colors (e.g. for redirecting to a file or a non-color terminal)
python3 viewer/viewer.py --source mock_data/mock_events.json --no-color
```

`--format auto` (the default) infers JSON-array vs. JSONL from the file
extension; pass `--format jsonl` explicitly if your file doesn't end in
`.jsonl`.

### Example output

```
------------------------------------------------------------
Agent     : Researcher-01
Operation : READ
Resource  : customer_pii.email
Decision  : DENY
Reason    : Agent does not hold READ:customer_pii capability; default-deny applies.
Reason Cd : MISSING_CAPABILITY
Trace ID  : trc-3c4d5e6f
Timestamp : 2026-08-22T09:00:09.771Z
Component : capability_manager
Data Class: PII
Latency   : 3.1 ms
------------------------------------------------------------

Summary: 10 event(s) loaded
  ALLOW     : 2
  DENY      : 5
  MODIFY    : 1
  THROTTLE  : 1
  TERMINATE : 1
```

`ALLOW` renders green, `DENY` and `TERMINATE` render red, `MODIFY` renders
yellow, `THROTTLE` renders magenta. Colors auto-disable when output isn't a
terminal (e.g. piped to a file) or when `--no-color` is passed.

This was actually run and verified during development, including: the full
mock dataset, JSONL one-shot mode, `--follow` picking up a line appended to
the file mid-run, the `--mock` fallback with zero files present, and
rejection of a malformed event missing required fields.

## 5. How mock events work

`mock_data/mock_events.json` is a synthetic dataset with 10 events, unique
trace IDs, and full coverage of the required demonstration scenarios:

1. `ALLOW` — legitimate `AGGREGATE` on `sales`
2. `ALLOW` — legitimate `READ` on `sales.region_summary`
3. `DENY` — missing capability (`READ customer_pii.email`)
4. `DENY` — PII export blocked (`EXPORT customer_pii.contact_records`)
5. `DENY` — explicit policy deny rule (`READ finance.unpublished_financials`)
6. `DENY` — classification violation (`READ employee.compensation_bands`)
7. `MODIFY` — field redacted from a `SELECT *`-style aggregate
8. `THROTTLE` — query budget nearing exhaustion
9. `TERMINATE` — query budget exceeded after a prior throttle
10. `DENY` — child agent denied reuse of parent's capabilities (capability isolation)

No real personal data is used anywhere; all names, emails, and financial
figures are placeholders/synthetic, per SRS §2.3 and NFR-09.

`mock_data/live_events.jsonl` is a small JSONL file used to demonstrate
`--follow`: run the viewer against it with `--follow`, then in another
terminal append a JSON line to the file — the viewer will print it as it
arrives.

## 6. How future real JÄGER events connect

The viewer never touches mock data directly — it only calls the
`EventSource` interface in `event_source.py`:

```
mock_events.json / live_events.jsonl
              |
              v
   EventSource implementation
   (JsonFileEventSource / JsonlFileEventSource / MockEventSource)
              |
              v
          viewer.py
              |
              v
        terminal output
```

To connect a real JAGER component later:

- **Simplest path:** have the Provenance Engine (or any component on the
  enforcement path) append one JSON object per line to a `.jsonl` file that
  conforms to `schema/event_schema.json`. Point the viewer at it with
  `--format jsonl --follow`. No viewer code changes needed.
- **Structured path:** implement a new class inheriting `EventSource` (e.g.
  `JagerRuntimeEventSource`) that calls into the real Provenance Engine's
  `get_trace()` / event subscription API (`subscribe_events()` per SRS
  Section 5.2) and yields the same event dict shape. `viewer.py` only calls
  `.events()` / `.follow()` and never needs to know the transport.

## 7. Mapping to the JÄGER SRS

| Requirement | What this MVP does |
|---|---|
| **FR-13 Provenance** | Not implemented here — provenance *capture* is the enforcement layer's job. This MVP defines and consumes the event shape that a provenance record could be projected into. **Designed for later integration.** |
| **FR-14 Audit queries** | The viewer's file-based load is a stand-in for an audit query. There is no query interface (filter by agent/time/decision) yet. **Partially implemented — file load only, no query language.** |
| **FR-21 Structured decision explanation** | Every mock event carries both `reason` (human-readable) and `reason_code` (machine-readable), and the viewer displays both. **Implemented in the event format and viewer display**, using synthetic data — the real reason codes must come from the actual Policy Engine. |
| **NFR-04 Traceability** | Every event has a unique `trace_id`; `parent_trace_id` is included for the child-agent scenario. **Implemented in the schema and mock data.** The viewer does not yet reconstruct a full trace graph across multiple events sharing a trace_id — that's next-iteration work. |
| **NFR-08 Decision explanation (usability)** | The terminal viewer renders a plain-language `Reason` alongside the `Reason Cd` for every decision, matching NFR-08's intent for the administrative console. **Implemented**, in terminal form rather than the full administrative console. |
| **NFR-11 Observability** | This *is* the observability layer's first cut: a common event schema plus a viewer. **Implemented for a single static/JSONL source.** Real-time ingestion from multiple concurrent components, and correlation across components for one trace_id, is **not yet implemented**. |
| **SR-05 Tamper-evident events** | **Not implemented.** This MVP has no signing, hashing, or append-only storage — a mock JSON/JSONL file is trivially editable. Tamper-evidence must be added at the Audit Store / Provenance Engine layer before this claim can be made. |
| **SR-12 Complete provenance for denied/modified requests** | The mock dataset intentionally gives DENY, MODIFY, THROTTLE, and TERMINATE events the *same field completeness* as ALLOW events (same schema, no fields omitted for non-ALLOW outcomes), demonstrating the intended shape. **Demonstrated with synthetic data; not verified against a real enforcement path**, since no real Policy Engine exists yet to test against.

**Explicitly not yet implemented:** authentication for the viewer/console,
a query language for FR-14, cross-event trace-graph reconstruction, tamper-evidence
(SR-05), and any live connection to a real JAGER component (only the
integration seam exists).

## 8. Architectural constraint honored

The viewer is not part of the security boundary. It cannot ALLOW, DENY,
MODIFY, THROTTLE, or TERMINATE anything — it only reads and prints events
that some other component already decided:

```
Agent
  |
  v
JAGER enforcement (Capability Manager / Policy Engine / ...)
  |
  +--> security decision
  |
  v
observability event  <-- this component starts here
  |
  v
viewer
```

## 9. Assumptions and limitations

- Python 3.10+, standard library only (`argparse`, `json`, `pathlib`, `abc`, `time`).
- `--follow` uses simple polling (`readline` + `sleep`), not `inotify` — fine
  for a first-hour MVP, not for production-scale tailing.
- The viewer validates that required fields are present and that `decision`
  is one of the five allowed values; it does not otherwise validate field
  *content* (e.g. it won't catch a `resource` string that doesn't match any
  real dataset).
- All data is synthetic; nothing here has been tested against a live Exasol
  connection or a real Policy Engine, since neither exists yet in this
  milestone.
