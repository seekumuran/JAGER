from .simulator_target import SimulatorTarget


class BlackBoxAdapter(SimulatorTarget):
    """
    JÄGER adapter for the synthetic black-box target.

    The simulator remains unaware of JÄGER.
    JÄGER only sees the public observe() interface.
    """

    def __init__(self, simulator):
        super().__init__(simulator)

    def probe(self, parameters):
        return self.observe(
            **parameters
        )
