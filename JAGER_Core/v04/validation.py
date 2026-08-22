REQUIRED_INPUTS = {
    "cpu_load",
    "memory_load",
    "num_processes",
    "num_threads",
    "ipc_intensity",
}


def validate_inputs(inputs):
    if set(inputs.keys()) != REQUIRED_INPUTS:
        return False

    if not 0 <= inputs["cpu_load"] <= 100:
        return False

    if not 0 <= inputs["memory_load"] <= 100:
        return False

    if not 0 <= inputs["ipc_intensity"] <= 100:
        return False

    if inputs["num_processes"] < 0:
        return False

    if inputs["num_threads"] < 0:
        return False

    if not isinstance(
        inputs["num_processes"],
        int,
    ):
        return False

    if not isinstance(
        inputs["num_threads"],
        int,
    ):
        return False

    return True
