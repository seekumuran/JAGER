from .models import Action
from .policy import SecurityPolicy


class SecurityGate:
    def __init__(self):
        self.policy = SecurityPolicy()

    def authorize(self, action: Action):
        return self.policy.evaluate(action)
