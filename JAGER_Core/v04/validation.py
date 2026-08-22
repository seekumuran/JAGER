from .errors import InvalidActionError


REQUIRED_INPUTS = {
    "cpu_load",
    "memory_load",
    "num_processes",
    "num_threads",
    "ipc_intensity",
}


def validate_inputs(inputs):
    if not isinstance(inputs, dict):
        raise InvalidActionError(
            "Inputs must be a dictionary."
        )

    missing = REQUIRED_INPUTS - set(inputs)

    if missing:
        raise InvalidActionError(
            f"Missing inputs: {sorted(missing)}"
        )

    cpu = inputs["cpu_load"]
    memory = inputs["memory_load"]
    processes = inputs["num_processes"]
    threads = inputs["num_threads"]
    ipc = inputs["ipc_intensity"]

    if not 0 <= cpu <= 100:
        raise InvalidActionError(
            "cpu_load must be between 0 and 100."
        )

    if not 0 <= memory <= 100:
        raise InvalidActionError(
            "memory_load must be between 0 and 100."
        )

    if not 0 <= ipc <= 100:
        raise InvalidActionError(
            "ipc_intensity must be between 0 and 100."
        )

    if not isinstance(processes, int) or processes < 0:
        raise InvalidActionError(
            "num_processes must be a non-negative integer."
        )

    if not isinstance(threads, int) or threads < 0:
        raise InvalidActionError(
            "num_threads must be a non-negative integer."
        )

    return True
