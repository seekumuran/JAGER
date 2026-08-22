# JÄGER — Black-Box Simulated Target

A tiny, self-contained simulator of a generic computer system. This is
**JÄGER's first black-box target**: something a policy engine, test harness,
or autonomous agent can be pointed at and observed, without access to (or
knowledge of) what's happening inside.

```
INPUT -> SIMULATED SYSTEM -> TELEMETRY / OUTCOME
```

This module does **not** include a hunter, an AI, a memory system, Linux
integration, or a sandbox. It is only the target being observed.

## Files

| File                        | Purpose                                                    |
|-----------------------------|-------------------------------------------------------------|
| `blackbox_system.py`        | The simulator itself (`SimulatedSystem` class)             |
| `example_run.py`            | Runs 10 experiments and prints inputs/telemetry/status     |
| `test_blackbox_system.py`   | Small unit test suite                                      |

## Inputs

| Input           | Range / Type          |
|------------------|------------------------|
| `cpu_load`       | 0–100 (float)          |
| `memory_load`    | 0–100 (float)          |
| `num_processes`  | non-negative integer   |
| `num_threads`    | non-negative integer   |
| `ipc_intensity`  | 0–100 (float)          |

## Outputs

Calling `observe(...)` returns a dict with exactly three keys:

```python
{
  "inputs": { ... echoed back ... },
  "telemetry": {
      "cpu_usage": ...,
      "memory_usage": ...,
      "latency_ms": ...,
      "process_count": ...,
      "thread_count": ...,
      "ipc_activity": ...,
  },
  "status": "NORMAL" | "DEGRADED" | "FAILED",
}
```

That's it. The simulator does not explain *why* a status was reached — it's a
black box on purpose. There is one hidden failure mode inside, triggered by a
combination of inputs rather than any single threshold, and it is not exposed
or documented outside of `blackbox_system.py` itself.

## How to run it

**Run the example (10 experiments):**
```bash
python3 example_run.py
```

**Run the tests:**
```bash
python3 -m unittest test_blackbox_system.py -v
```

**Use it directly:**
```python
from blackbox_system import SimulatedSystem

system = SimulatedSystem(seed=42)
result = system.observe(
    cpu_load=70,
    memory_load=70,
    num_processes=100,
    num_threads=180,
    ipc_intensity=80,
)
print(result)
```

## Reproducibility

`SimulatedSystem(seed=42)` seeds an internal RNG. Two instances created with
the same seed, called with the same inputs in the same order, will always
produce identical output — useful for regression tests and for comparing
a "hunter"/policy engine's behavior across repeated runs against a fixed
target.

## Handoff notes

- This module is intentionally tiny (2 Python files + 1 test file). Nothing
  about probing strategy, detection, or enforcement belongs here — that's
  for whichever component consumes this simulator's output next.
- If you extend this later with more hidden fault modes, keep the same
  discipline: the fault logic lives in a private method, and the public
  `observe()` return value never grows a field that leaks it.
