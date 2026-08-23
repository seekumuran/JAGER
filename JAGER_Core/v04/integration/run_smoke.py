from .end_to_end import (
    EndToEndRunner,
    build_mock_runtime,
)


def main():

    jager = build_mock_runtime()

    runner = EndToEndRunner(
        jager
    )

    health = runner.health_check()

    print(
        "JÄGER HEALTH"
    )

    print(
        health
    )

    if not health["healthy"]:

        raise SystemExit(
            "JÄGER health check failed"
        )

    result = runner.run(
        target="mock",
        objective=(
            "Validate complete "
            "JÄGER execution path."
        ),
        maximum_iterations=1,
    )

    print(
        "JÄGER SMOKE TEST"
    )

    print(
        result
    )


if __name__ == "__main__":
    main()
