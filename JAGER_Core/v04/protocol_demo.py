from blackbox_system import SimulatedSystem

from .blackbox_adapter import (
    BlackBoxAdapter,
)
from .config import JagerConfig
from .integration import JagerRuntime


def main():

    simulator = SimulatedSystem(
        seed=42
    )

    target = BlackBoxAdapter(
        simulator
    )

    runtime = JagerRuntime(
        config=JagerConfig(
            seed=42,
            budget=20,
        )
    )

    runtime.attach_target(
        "blackbox",
        target,
    )

    result = runtime.run_protocol(
        "blackbox"
    )

    print()
    print("=" * 60)
    print("JÄGER v0.4 — EXPERIMENT PROTOCOL")
    print("=" * 60)

    print(
        "Final state:",
        result["state"],
    )

    print(
        "State history:"
    )

    for state in result["history"]:
        print(
            f"  -> {state}"
        )

    print()
    print("Protocol events:")

    for event in result["events"]:
        print(
            f"[{event['step']}] "
            f"{event['status']}"
        )

    print()
    print(
        "Experiments:",
        len(
            runtime.hunter.experiments
        ),
    )

    print(
        "Discoveries:",
        len(
            runtime.hunter.failed_discoveries
        ),
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
