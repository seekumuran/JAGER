import hashlib
import json
import platform
import sys
import time


class ReproducibilityManifest:

    VERSION = "0.4.0"

    def __init__(
        self,
        run_id,
        seed,
        budget,
        target,
    ):
        self.run_id = run_id
        self.seed = seed
        self.budget = budget
        self.target = target

    def generate(self):
        return {
            "jager_version": self.VERSION,
            "run_id": self.run_id,
            "seed": self.seed,
            "budget": self.budget,
            "target": self.target,
            "environment": {
                "python": sys.version,
                "platform": platform.platform(),
                "architecture": platform.machine(),
            },
            "created_at": time.time(),
        }

    def fingerprint(self):
        manifest = self.generate()

        canonical = json.dumps(
            manifest,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()
