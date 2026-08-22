from blackbox_system import (
    SimulatedSystem,
)

from .sandbox.ai_sandbox import (
    AISandbox,
)

from .targets import (
    BlackBoxTarget,
    LinuxTarget,
)


def register_default_targets(runtime):

    runtime.register_target(
        BlackBoxTarget(
            SimulatedSystem(
                seed=runtime.config.seed
            )
        )
    )

    runtime.register_target(
        LinuxTarget()
    )

    runtime.register_target(
        AISandbox(
            seed=runtime.config.seed
        )
    )

    return runtime
