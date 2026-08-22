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

    print()
    print("=" * 60)
    print("JÄGER v0.4 — TARGET SELECTION")
    print("=" * 60)

    print(
        "Available:",
        ", ".join(
            runtime.available_targets()
        ),
    )

    for target_name in (
        "blackbox",
        "linux",
        "ai_sandbox",
    ):

        target = runtime.select_target(
            target_name
        )

        print()
        print(
            f"Selected: {target.name}"
        )

        if target_name == "blackbox":

            result = (
                runtime.observe_target(
                    cpu_load=20,
                    memory_load=30,
                    num_processes=10,
                    num_threads=20,
                    ipc_intensity=10,
                )
            )

        else:

            result = (
                runtime.observe_target()
            )

        print(
            "Status:",
            result["status"],
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
