import argparse
import json
import sys

from .bootstrap import (
    JagerBootstrap,
)


def build_parser():

    parser = argparse.ArgumentParser(
        prog="jager",
        description="JAGER runtime",
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--debug",
        action="store_true",
    )

    parser.add_argument(
        "--snapshot",
        action="store_true",
    )

    return parser


def main(
    argv=None,
):

    parser = build_parser()

    args = parser.parse_args(
        argv
    )

    overrides = {}

    if args.debug:

        overrides["debug"] = True

    bootstrap = JagerBootstrap(
        config_path=args.config,
        overrides=overrides,
    )

    try:

        jager = bootstrap.initialize()

        if args.snapshot:

            print(
                json.dumps(
                    jager.snapshot(),
                    indent=2,
                    default=str,
                )
            )

        else:

            print(
                "JAGER started successfully."
            )

        return 0

    except Exception as exc:

        print(
            f"JAGER startup failed: {exc}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
