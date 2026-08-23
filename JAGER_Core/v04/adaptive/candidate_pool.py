from typing import Dict, List, Optional

from .candidate import Candidate


class CandidatePool:

    def __init__(
        self,
        maximum_size: int = 1000,
    ):

        if maximum_size <= 0:
            raise ValueError(
                "maximum_size must be positive"
            )

        self.maximum_size = maximum_size

        self._items: Dict[
            str, Candidate
        ] = {}

    def add(
        self,
        candidate: Candidate,
    ):

        self._items[
            candidate.candidate_id
        ] = candidate

        self._trim()

    def add_many(
        self,
        candidates: List[Candidate],
    ):

        for candidate in candidates:
            self.add(candidate)

    def get(
        self,
        candidate_id: str,
    ) -> Optional[Candidate]:

        return self._items.get(
            candidate_id
        )

    def remove(
        self,
        candidate_id: str,
    ):

        self._items.pop(
            candidate_id,
            None,
        )

    def all(self) -> List[Candidate]:

        return list(
            self._items.values()
        )

    def size(self) -> int:

        return len(self._items)

    def clear(self):

        self._items.clear()

    def _trim(self):

        if self.size() <= (
            self.maximum_size
        ):
            return

        excess = (
            self.size()
            - self.maximum_size
        )

        ids = list(
            self._items.keys()
        )[:excess]

        for candidate_id in ids:
            self.remove(candidate_id)
