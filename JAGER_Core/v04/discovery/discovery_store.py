from typing import Dict, List, Optional

from .discovery_record import (
    DiscoveryRecord,
)


class DiscoveryStore:

    def __init__(
        self,
        maximum_size: int = 10000,
    ):

        if maximum_size <= 0:
            raise ValueError(
                "maximum_size must be positive"
            )

        self.maximum_size = (
            maximum_size
        )

        self._records: Dict[
            str, DiscoveryRecord
        ] = {}

    def add(
        self,
        discovery: DiscoveryRecord,
    ):

        self._records[
            discovery.discovery_id
        ] = discovery

        self._trim()

        return discovery

    def get(
        self,
        discovery_id: str,
    ) -> Optional[
        DiscoveryRecord
    ]:

        return self._records.get(
            discovery_id
        )

    def all(self):

        return list(
            self._records.values()
        )

    def for_target(
        self,
        target: str,
    ):

        return [
            item
            for item in self._records.values()
            if item.target == target
        ]

    def for_experiment(
        self,
        experiment_id: str,
    ):

        return [
            item
            for item in self._records.values()
            if item.experiment_id
            == experiment_id
        ]

    def size(self):

        return len(self._records)

    def _trim(self):

        while (
            len(self._records)
            > self.maximum_size
        ):

            oldest = min(
                self._records.values(),
                key=lambda item:
                    item.created_at,
            )

            del self._records[
                oldest.discovery_id
            ]
