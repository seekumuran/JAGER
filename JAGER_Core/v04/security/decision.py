from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SecurityDecision:

    allowed: bool
    action: str
    reason: str
    risk: float

    def to_dict(self) -> Dict[str, Any]:

        return {
            "allowed": self.allowed,
            "action": self.action,
            "reason": self.reason,
            "risk": self.risk,
        }
