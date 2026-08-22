import argparse
from pathlib import Path

from .config import JagerConfig
from .export import export_run
from .hunter import JagerHunter


def build_parser():
    parser = argparse.ArgumentParser(
        description="JÄGER v0.4 experiment runner"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--budget",
        type=int,
        default=1000,
    )

    parser.add_argument(
        "--output",
        type=str,
        default="JAGER_Core/v04/results",
    )

    return parser


def main():
    args = build_parser().parse_args()

    config = JagerConfig(
        seed=args.seed,
        budget=args.budget,
    )

    hunter = JagerHunter(
        seed=config.seed,
        budget=config.budget,
    )

    discoveries = hunter.run()

    output_dir = Path(args.output)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_dir / f"{hunter.run_id}.json"

    export_run(
        output_file,
        hunter,
    )

    print("=" * 65)
    print("JÄGER v0.4 EXPERIMENT")
    print("=" * 65)
    print(f"Run ID:             {hunter.run_id}")
    print(f"Seed:               {config.seed}")
    print(f"Budget:             {config.budget}")
    print(f"Experiments:        {len(hunter.experiments)}")
    print(f"Memory entries:     {len(hunter.memory)}")
    print(f"Discoveries:        {len(discoveries)}")
    print(f"Events:             {len(hunter.logger.events)}")
    print(f"Output:             {output_file}")
    print("=" * 65)


if __name__ == "__main__":
    main()
