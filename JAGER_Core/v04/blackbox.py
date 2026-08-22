from blackbox_system import SimulatedSystem

from .blackbox_adapter import BlackBoxAdapter
from .config import JagerConfig
from .integration import JagerRuntime


def main():

    # -----------------------------------------
    # Create the black-box target
    # -----------------------------------------

    simulator = SimulatedSystem(
        seed=42
    )

    target = BlackBoxAdapter(
        simulator
    )

    # -----------------------------------------
    # Create JÄGER
    # -----------------------------------------

    config = JagerConfig(
        seed=42,
        budget=25,
    )

    runtime = JagerRuntime(
        config=config
    )

    runtime.attach_target(
        "blackbox",
        target,
    )

    # -----------------------------------------
    # Run JÄGER
    # -----------------------------------------

    discoveries = runtime.start(
        "blackbox"
    )

    # -----------------------------------------
    # Display results
    # -----------------------------------------

    print()
    print("=" * 60)
    print("JÄGER v0.4 — BLACK-BOX EXPERIMENT")
    print("=" * 60)

    print(
        f"Run ID: "
        f"{runtime.hunter.run_id}"
    )

    print(
        f"Experiments: "
        f"{len(runtime.hunter.experiments)}"
    )

    print(
        f"Discoveries: "
        f"{len(discoveries)}"
    )

    print()

    for discovery in discoveries:
        print("-" * 60)

        print(
            "Experiment:",
            discovery["experiment_id"],
        )

        print(
            "Trace:",
            discovery["trace_id"],
        )

        print(
            "Inputs:",
            discovery["action"].parameters,
        )

        print(
            "Status:",
            discovery[
                "observation"
            ].status,
        )

        print(
            "Reward:",
            discovery[
                "experience"
            ].reward,
        )

    print()
    print("=" * 60)

    print(
        "FINAL STATE"
    )

    print(
        runtime.status()
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
