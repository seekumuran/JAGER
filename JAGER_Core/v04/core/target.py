from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Target:

    target_id: str

    name: str

    kind: str = "unknown"

    endpoint: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    active: bool = True

    def activate(self):

        self.active = True

    def deactivate(self):

        self.active = False

    def snapshot(self):

        return {
            "target_id":
                self.target_id,
            "name":
                self.name,
            "kind":
                self.kind,
            "endpoint":
                self.endpoint,
            "active":
                self.active,
            "metadata":
                dict(self.metadata),
        }


class TargetRegistry:

    def __init__(self):

        self._targets: Dict[
            str,
            Target,
        ] = {}

    def register(
        self,
        target: Target,
    ):

        if target.target_id in self._targets:

            raise ValueError(
                "target already registered: "
                f"{target.target_id}"
            )

        self._targets[
            target.target_id
        ] = target

        return target

    def get(
        self,
        target_id: str,
    ):

        return self._targets.get(
            target_id
        )

    def remove(
        self,
        target_id: str,
    ):

        return self._targets.pop(
            target_id,
            None,
        )

    def all(self):

        return list(
            self._targets.values()
        )

    def active(self):

        return [
            target
            for target in self._targets.values()
            if target.active
        ]

    def snapshot(self):

        return {
            target_id:
                target.snapshot()
            for target_id, target
            in self._targets.items()
        }
