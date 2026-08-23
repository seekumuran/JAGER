from threading import RLock
from typing import Dict, List, Optional


class TargetRegistry:

    def __init__(self):

        self._targets: Dict[
            str,
            object,
        ] = {}

        self._lock = RLock()

    def register(
        self,
        target,
    ):

        if target is None:
            raise ValueError(
                "target cannot be None"
            )

        name = getattr(
            target,
            "name",
            None,
        )

        if not name:
            raise ValueError(
                "target must expose a non-empty name"
            )

        with self._lock:

            if name in self._targets:
                raise ValueError(
                    f"Target already registered: "
                    f"{name}"
                )

            self._targets[name] = target

        return target

    def unregister(
        self,
        name: str,
    ):

        with self._lock:

            return self._targets.pop(
                name,
                None,
            )

    def get(
        self,
        name: str,
    ) -> Optional[object]:

        with self._lock:

            return self._targets.get(
                name
            )

    def require(
        self,
        name: str,
    ):

        target = self.get(name)

        if target is None:

            raise KeyError(
                f"Unknown target: {name}"
            )

        return target

    def contains(
        self,
        name: str,
    ) -> bool:

        return self.get(name) is not None

    def names(self) -> List[str]:

        with self._lock:

            return sorted(
                self._targets.keys()
            )

    def values(self):

        with self._lock:

            return list(
                self._targets.values()
            )

    def size(self) -> int:

        with self._lock:

            return len(
                self._targets
            )

    def clear(self):

        with self._lock:

            self._targets.clear()
