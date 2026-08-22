from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class Capability:

    name: str
    operations: Set[str] = field(
        default_factory=set
    )

    def supports(
        self,
        operation: str,
    ) -> bool:
        return operation in self.operations


class CapabilityGraph:

    def __init__(self):

        self._targets: Dict[
            str, Dict[str, Capability]
        ] = {}

    def register(
        self,
        target: str,
        capability: str,
        operations: List[str],
    ):

        if target not in self._targets:
            self._targets[target] = {}

        self._targets[target][
            capability
        ] = Capability(
            name=capability,
            operations=set(operations),
        )

    def capabilities(
        self,
        target: str,
    ) -> List[str]:

        return sorted(
            self._targets.get(
                target,
                {},
            ).keys()
        )

    def operations(
        self,
        target: str,
    ) -> List[str]:

        operations = set()

        for capability in self._targets.get(
            target,
            {},
        ).values():

            operations.update(
                capability.operations
            )

        return sorted(operations)

    def supports(
        self,
        target: str,
        operation: str,
    ) -> bool:

        return any(
            capability.supports(
                operation
            )
            for capability in self._targets.get(
                target,
                {},
            ).values()
        )

    def describe(
        self,
        target: str,
    ):

        result = {}

        for name, capability in (
            self._targets.get(
                target,
                {},
            ).items()
        ):

            result[name] = sorted(
                capability.operations
            )

        return result
