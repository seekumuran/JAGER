from .action_generator import (
    ActionGenerator,
)

from .config import JagerConfig

from .integration import (
    JagerRuntime,
)

from .runtime_targets import (
    register_default_targets,
)


def main():

    runtime = JagerRuntime(
        config=JagerConfig(
            seed=42,
            budget=20,
        )
    )

    register_default_targets(
        runtime
    )

    runtime.select_target(
        "blackbox"
    )

    generator = ActionGenerator(
        seed=42
    )

    def candidates():

        return [
            generator.generate(
                "blackbox"
            )
            for _ in range(5)
        ]

    results = (
        runtime.run_adaptive_experiments(
            candidates,
            20,
        )
    )

    print()
    print("=" * 70)
    print(
        "JÄGER v0.4 — ADAPTIVE SEARCH"
    )
    print("=" * 70)

    for result in results:

        print(
            f"{result['experiment_id']} | "
            f"reward="
            f"{result['reward']:.2f} | "
            f"novelty="
            f"{result['novelty']:.2f}"
        )

    print()
    print("SEARCH STATISTICS")

    for key, value in (
        runtime.search
        .statistics()
        .items()
    ):

        print(
            value
        )

    print("=" * 70)


if __name__ == "__main__":
    main()
