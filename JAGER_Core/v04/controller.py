from .audit import AuditTrail
from .config import JagerConfig
from .metrics import Metrics
from .state import HunterState


class HunterController:
    def __init__(self, config: JagerConfig):
        self.config = config
        self.state = HunterState()
        self.metrics = Metrics()
        self.audit = AuditTrail()

    def allowed(self):
        self.state.record_allowed()
        self.metrics.record_decision(True)

    def denied(self):
        self.state.record_denied()
        self.metrics.record_decision(False)

    def experiment(self, status, reward):
        self.state.record_experiment(reward)
        self.metrics.record_status(status)

    def discovery(self, confirmed):
        self.state.record_discovery(confirmed)

    def summary(self):
        return {
            "state": self.state,
            "metrics": self.metrics.snapshot(),
            "discovery_rate": self.metrics.discovery_rate(),
            "audit_events": len(self.audit),
        }
