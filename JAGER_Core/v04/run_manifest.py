from dataclasses import asdict, dataclass
import platform
import sys
import time


@dataclass
class RunManifest:
    run_id: str
    seed: int
    budget: int
    version: str = "0.4.0"
    python_version: str = sys.version
    platform: str = platform.platform()
    created_at: float = 0.0

    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()

    def to_dict(self):
        return asdict(self)
