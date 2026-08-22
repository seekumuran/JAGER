from .config import JagerConfig
from .integration import JagerRuntime
from .runtime_targets import (
    register_default_targets,
)


def main():

    runtime = JagerRuntime(
        config=JagerConfig(
            seed=42,
            budget=10,
        )
    )

    register_default_targets(
        runtime
    )

    runtime.select_target(
        "blackbox"
    )

    results = (
        runtime.run_experiments(
            10
        )
    )

    print()
    print("=" * 70)
    print("JÄGER v0.4 — END-TO-END RUN")
    print("=" * 70)

    for result in results:

        observation = result[
            "observation"
        ]

        print(
            f"{result['experiment_id']} | "
            f"{observation['status']:8} | "
            f"reward="
            f"{result['reward']:.2f} | "
            f"novelty="
            f"{result['novelty']:.2f}"
        )

    print("=" * 70)

    print(
        f"Experiments: "
        f"{len(results)}"
    )


if __name__ == "__main__":
    main()
