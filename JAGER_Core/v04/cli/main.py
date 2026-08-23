import argparse
import json
import sys
from pathlib import Path

from ..api.jager import Jager
from ..config.config_loader import ConfigLoader
from ..config.defaults import default_config
from ..executor.mock_target import MockTarget
from ..executor.registry import TargetRegistry


def build_registry():
    registry = TargetRegistry()

    registry.register(
        MockTarget("mock")
    )

    return registry


def build_parser():

    parser = argparse.ArgumentParser(
        prog="jager",
        description=(
            "JÄGER autonomous "
            "experiment and learning runtime."
        ),
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to a JSON configuration file.",
    )

    parser.add_argument(
        "--state",
        type=str,
        default="data/runtime_state.json",
        help="Path to persistent runtime state.",
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Run an adaptive experiment.",
    )

    run_parser.add_argument(
        "target",
        help="Target name.",
    )

    run_parser.add_argument(
        "objective",
        help="Experiment objective.",
    )

    run_parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Maximum experiment iterations.",
    )

    run_parser.add_argument(
        "--maximum-risk",
        type=float,
        default=None,
        help="Maximum permitted risk.",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Show runtime state.",
    )

    status_parser.set_defaults(
        command="status"
    )

    targets_parser = subparsers.add_parser(
        "targets",
        help="List registered targets.",
    )

    targets_parser.set_defaults(
        command="targets"
    )

    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset persistent runtime state.",
    )

    reset_parser.set_defaults(
        command="reset"
    )

    return parser


def load_config(path):

    if path is None:
        return default_config()

    return ConfigLoader().load_file(
        path
    )


def main(argv=None):

    parser = build_parser()

    args = parser.parse_args(argv)

    if args.command is None:

        parser.print_help()

        return 0

    try:

        config = load_config(
            args.config
        )

        registry = build_registry()

        jager = Jager(
            registry=registry,
            config=config,
            state_path=args.state,
        )

        if args.command == "run":

            constraints = {}

            if args.maximum_risk is not None:

                constraints[
                    "maximum_risk"
                ] = args.maximum_risk

            result = jager.run(
                target=args.target,
                objective=args.objective,
                constraints=constraints,
                maximum_iterations=
                    args.iterations,
            )

            print(
                json.dumps(
                    result,
                    indent=2,
                    default=str,
                )
            )

            return 0

        if args.command == "status":

            print(
                json.dumps(
                    jager.status(),
                    indent=2,
                    default=str,
                )
            )

            return 0

        if args.command == "targets":

            for target in jager.targets():
                print(target)

            return 0

        if args.command == "reset":

            jager.reset()

            print(
                "JÄGER runtime state reset."
            )

            return 0

        parser.print_help()

        return 1

    except Exception as exc:

        print(
            f"JÄGER error: {exc}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
