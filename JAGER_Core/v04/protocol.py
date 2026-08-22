from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ProtocolStep:
    name: str
    description: str
    required: bool = True


@dataclass
class ExperimentProtocol:
    name: str = "JAGER Black-Box Discovery Protocol"
    version: str = "1.0"
    steps: List[ProtocolStep] = field(
        default_factory=lambda: [
            ProtocolStep(
                name="INITIALIZE",
                description="Initialize JÄGER and the target.",
            ),
            ProtocolStep(
                name="BASELINE",
                description="Collect baseline observations.",
            ),
            ProtocolStep(
                name="EXPLORE",
                description="Explore the target input space.",
            ),
            ProtocolStep(
                name="REFINE",
                description="Refine search around interesting behavior.",
            ),
            ProtocolStep(
                name="VERIFY",
                description="Re-test candidate discoveries.",
            ),
            ProtocolStep(
                name="FINALIZE",
                description="Generate the experiment summary.",
            ),
        ]
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "steps": [
                {
                    "name": step.name,
                    "description": step.description,
                    "required": step.required,
                }
                for step in self.steps
            ],
        }

    def step_names(self) -> List[str]:
        return [
            step.name
            for step in self.steps
        ]

    def validate(self) -> bool:
        names = self.step_names()

        if not names:
            raise ValueError(
                "Protocol must contain at least one step."
            )

        if len(names) != len(set(names)):
            raise ValueError(
                "Protocol step names must be unique."
            )

        return True
