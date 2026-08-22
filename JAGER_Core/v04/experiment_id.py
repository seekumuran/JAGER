import uuid


def generate_experiment_id(counter):
    return f"exp-{counter:08d}"


def generate_run_id():
    return f"run-{uuid.uuid4().hex[:16]}"


def generate_trace_id():
    return f"trace-{uuid.uuid4().hex[:16]}"
