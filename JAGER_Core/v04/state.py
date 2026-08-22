from dataclasses import dataclass


@dataclass
class HunterState:
    experiments: int = 0
    discoveries: int = 0
    confirmed_discoveries: int = 0
    allowed_actions: int = 0
    denied_actions: int = 0
    total_reward: float = 0.0

    def record_allowed(self):
        self.allowed_actions += 1

    def record_denied(self):
        self.denied_actions += 1

    def record_experiment(self, reward: float):
        self.experiments += 1
        self.total_reward += reward

    def record_discovery(self, confirmed: bool):
        self.discoveries += 1

        if confirmed:
            self.confirmed_discoveries += 1
