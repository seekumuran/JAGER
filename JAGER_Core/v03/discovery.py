from .models import Discovery


class DiscoveryManager:
    def __init__(self):
        self.counter = 0
        self.discoveries = []

    def evaluate(
        self,
        experiment_id,
        inputs,
        status,
    ):
        if status != "FAILED":
            return None

        self.counter += 1

        discovery = Discovery(
            discovery_id=f"D-{self.counter:05d}",
            experiment_id=experiment_id,
            inputs=inputs,
            status=status,
            confirmed=False,
        )

        self.discoveries.append(discovery)

        return discovery

    def confirm(
        self,
        discovery: Discovery,
        reproduction_attempts: int,
    ):
        discovery.reproduction_attempts = reproduction_attempts
        discovery.confirmed = reproduction_attempts > 0
        return discovery
