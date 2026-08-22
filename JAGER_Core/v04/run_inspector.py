import json
import sys


def inspect_run(path):

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as handle:

        data = json.load(handle)

    summary = data[
        "summary"
    ]

    print()
    print("=" * 60)
    print("JÄGER RUN INSPECTOR")
    print("=" * 60)

    print(
        f"Run ID:       {summary['run_id']}"
    )

    print(
        f"Version:      {summary['jager_version']}"
    )

    print(
        f"Target:       {summary['target']}"
    )

    print(
        f"Seed:         {summary['seed']}"
    )

    print(
        f"Budget:       {summary['budget']}"
    )

    print()

    print(
        f"Experiments:  {summary['experiments']}"
    )

    print(
        f"Candidates:   {summary['candidates']}"
    )

    print(
        f"Verified:     {summary['verified']}"
    )

    print()

    print(
        f"NORMAL:       {summary['normal']}"
    )

    print(
        f"DEGRADED:     {summary['degraded']}"
    )

    print(
        f"FAILED:       {summary['failed']}"
    )

    print("=" * 60)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m "
            "JAGER_Core.v04.run_inspector "
            "<run.json>"
        )
        raise SystemExit(1)

    inspect_run(
        sys.argv[1]
    )
