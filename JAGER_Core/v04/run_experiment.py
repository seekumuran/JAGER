from pathlib import Path

from .config import JagerConfig
from .export import export_run
from .hunter import JagerHunter


def run_experiment(config=None):
    config = config or JagerConfig()

    hunter = JagerHunter(
        seed=config.seed,
        budget=config.budget,
    )

    discoveries = hunter.run()

    output = Path(
        "JAGER_Core"
    ) / "v04" / "results" / f"{hunter.run_id}.json"

    export_run(
        output,
        hunter,
    )

    return hunter, discoveries, output
