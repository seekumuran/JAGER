from pathlib import Path

from .serialization import dumps


def export_run(
    output_path,
    hunter,
):
    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "run_id": hunter.run_id,
        "seed": hunter.seed,
        "budget": hunter.budget,
        "experiments": hunter.experiments,
        "events": hunter.logger.export(),
        "discoveries": hunter.failed_discoveries,
        "memory_size": len(hunter.memory),
    }

    path.write_text(
        dumps(data),
        encoding="utf-8",
    )

    return path
