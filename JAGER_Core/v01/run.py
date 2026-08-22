import json
from pathlib import Path
from datetime import datetime

from .baseline_hunter import BaselineHunter


def main():
    seed = 42
    budget = 1000

    hunter = BaselineHunter(
        seed=seed,
        budget=budget,
    )

    print("=" * 50)
    print("JÄGER v0.1 — BASELINE HUNTER")
    print("=" * 50)
    print(f"Run ID: {hunter.run_id}")
    print(f"Seed: {seed}")
    print(f"Budget: {budget}")
    print()

    discovery = hunter.run()

    for record in hunter.experiments:
        print(
            f"[{record.experiment_id}] "
            f"{record.status}"
        )

    print()
    print("=" * 50)
    print("RESULT")
    print("=" * 50)

    if discovery:
        print("Status: DISCOVERY FOUND")
        print(f"Experiment: {discovery.experiment_id}")
    else:
        print("Status: NO DISCOVERY")
        print("The experiment budget was exhausted.")

    print(f"Experiments executed: {len(hunter.experiments)}")
    print(f"Unique discoveries: {len(hunter.discoveries)}")

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    output_file = results_dir / f"{hunter.run_id}.jsonl"

    with output_file.open("w", encoding="utf-8") as file:
        for record in hunter.experiments:
            file.write(json.dumps(record.to_dict()) + "\n")

    print(f"Results: {output_file}")


if __name__ == "__main__":
    main()
