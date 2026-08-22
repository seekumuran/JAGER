from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TargetDescriptor:

    name: str
    version: str
    description: str
    environment: str
    capabilities: List[str]


class TargetCatalog:

    def __init__(self):

        self._targets: Dict[
            str, TargetDescriptor
        ] = {}

    def add(
        self,
        descriptor: TargetDescriptor,
    ):

        self._targets[
            descriptor.name
        ] = descriptor

    def get(
        self,
        name: str,
    ):

        return self._targets.get(
            name
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._targets

    def names(self):

        return sorted(
            self._targets.keys()
        )

    def describe_all(self):

        return {
            name: {
                "version":
                    descriptor.version,
                "description":
                    descriptor.description,
                "environment":
                    descriptor.environment,
                "capabilities":
                    descriptor.capabilities,
            }
            for name, descriptor
            in self._targets.items()
        }
