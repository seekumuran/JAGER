from .target import Target, TargetCapabilities


class SimulatorTarget(Target):
    """
    Adapter around the existing black-box simulator.

    JÄGER interacts with this through the generic
    Target interface rather than importing simulator
    implementation details.
    """

    def __init__(self, simulator):
        self.simulator = simulator

        self.capabilities = TargetCapabilities(
            name="blackbox-simulator",
            version="1.0",
            description=(
                "Synthetic black-box computer system "
                "used for reproducible JÄGER experiments."
            ),
        )

    def observe(self, **inputs):
        return self.simulator.observe(
            **inputs
        )

    def describe(self):
        return self.capabilities.to_dict()
