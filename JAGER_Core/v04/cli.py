import argparse
import json

from .hunter import JagerHunter


def main():
    parser = argparse.ArgumentParser(
        prog="jager",
        description="JÄGER autonomous research prototype",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = subparsers.add_parser("run")

    run_parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    run_parser.add_argument(
        "--budget",
        type=int,
        default=100,
    )

    args = parser.parse_args()

    if args.command == "run":
        hunter = JagerHunter(
            seed=args.seed,
            budget=args.budget,
        )

        discoveries = hunter.run()

        print(
            json.dumps(
                {
                    "run_id": hunter.run_id,
                    "experiments": len(
                        hunter.experiments
                    ),
                    "memory": len(hunter.memory),
                    "discoveries": len(discoveries),
                    "events": len(
                        hunter.logger.events
                    ),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
