from .linux_target import (
    LinuxTarget,
)


def main():

    target = LinuxTarget()

    result = target.observe()

    print()
    print("=" * 60)
    print("JÄGER v0.4 — LINUX TARGET")
    print("=" * 60)

    print(
        "Target:",
        target.name,
    )

    print(
        "Status:",
        result["status"],
    )

    print()

    for key, value in (
        result["telemetry"]
        .items()
    ):
        print(
            f"{key:16} {value}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
