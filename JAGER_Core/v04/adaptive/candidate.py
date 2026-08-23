from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Candidate:

    candidate_id: str
    target: str
    parameters: Dict[str, Any]
    source: str = "random"
    parent_id: str | None = None

    def to_action(self):

        return {
            "type": "probe",
            "parameters": dict(
                self.parameters
            ),
        }

    def to_dict(self):

        return {
            "candidate_id":
                self.candidate_id,
            "target":
                self.target,
            "parameters":
                dict(self.parameters),
            "source":
                self.source,
            "parent_id":
                self.parent_id,
        }
