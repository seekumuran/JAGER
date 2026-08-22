from blackbox_system import (
    SimulatedSystem,
)

from .blackbox_adapter import (
    BlackBoxAdapter,
)

from .config import (
    JagerConfig,
)

from .integration import (
    JagerRuntime,
)

from .multi_run import (
    MultiRunExperiment,
)

from .multi_run_writer import (
    MultiRunWriter,
)


def create_runtime(seed):

    simulator = SimulatedSystem(
        seed=seed
    )

    target = BlackBoxAdapter(
        simulator
    )

    runtime = JagerRuntime(
        config=JagerConfig(
            seed=seed,
            budget=25,
        )
    )

    runtime.attach_target(
        "blackbox",
        target,
    )

    return runtime


def main():

    experiment = MultiRunExperiment(
        runtime_factory=create_runtime,
        target_name="blackbox",
        seeds=[
            11,
            22,
            33,
            44,
            55,
        ],
    )

    experiment.run()

    writer = MultiRunWriter()

    path = writer.write(
        experiment,
        "multi_run_results.json",
    )

    print()
    print("=" * 60)
    print(
        "JÄGER v0.4 — MULTI-RUN EXPERIMENT"
    )
    print("=" * 60)

    for result in experiment.results:

        print(
            f"Seed {result.seed:>3} | "
            f"Experiments "
            f"{result.experiments:>3} | "
            f"Candidates "
            f"{result.candidates:>3} | "
            f"Verified "
            f"{result.verified:>3}"
        )

    print()

    summary = experiment.summary()

    print(
        f"Runs: "
        f"{summary['runs']}"
    )

    print(
        f"Total experiments: "
        f"{summary['total_experiments']}"
    )

    print(
        f"Total verified: "
        f"{summary['total_verified']}"
    )

    print(
        f"Mean discovery rate: "
        f"{summary['average_discovery_rate']:.4f}"
    )

    print(
        f"Mean verification rate: "
        f"{summary['average_verification_rate']:.4f}"
    )

    print(
        f"Mean reward: "
        f"{summary['average_reward']:.4f}"
    )

    print(
        f"Mean novelty: "
        f"{summary['average_novelty']:.4f}"
    )

    print()
    print(
        f"Saved: {path}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
