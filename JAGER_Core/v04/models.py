from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Action:
    action_id: str
    operation: str
    parameters: Dict[str, Any]
    risk: float = 0.0


@dataclass
class Observation:
    observation_id: str
    action_id: str
    telemetry: Dict[str, Any]
    status: str
    timestamp: float


@dataclass
class Experience:
    observation_id: str
    action: Action
    observation: Observation
    reward: float
    novelty: float
    useful: bool


@dataclass
class SecurityDecision:
    allowed: bool
    reason: str
    risk: float


@dataclass
class Event:
    event_id: str
    trace_id: str
    event_type: str
    operation: str
    decision: str
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)
