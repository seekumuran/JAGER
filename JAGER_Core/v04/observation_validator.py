from .errors import InvalidObservationError


REQUIRED_FIELDS = {
    "cpu_usage",
    "memory_usage",
    "latency_ms",
    "process_count",
    "thread_count",
    "ipc_activity",
}


VALID_STATUSES = {
    "NORMAL",
    "DEGRADED",
    "FAILED",
}


def validate_observation(result):
    if not isinstance(result, dict):
        raise InvalidObservationError(
            "Target result must be a dictionary."
        )

    required = {
        "inputs",
        "telemetry",
        "status",
    }

    missing = required - set(result)

    if missing:
        raise InvalidObservationError(
            f"Missing fields: {sorted(missing)}"
        )

    telemetry = result["telemetry"]

    missing_telemetry = (
        REQUIRED_FIELDS - set(telemetry)
    )

    if missing_telemetry:
        raise InvalidObservationError(
            "Missing telemetry fields: "
            f"{sorted(missing_telemetry)}"
        )

    if result["status"] not in VALID_STATUSES:
        raise InvalidObservationError(
            f"Invalid status: {result['status']}"
        )

    return True
