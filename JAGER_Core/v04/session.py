import uuid
import time


class HunterSession:
    def __init__(self, seed, budget):
        self.session_id = (
            f"session-{uuid.uuid4().hex[:12]}"
        )

        self.started_at = time.time()
        self.seed = seed
        self.budget = budget
        self.completed = False

    def finish(self):
        self.completed = True

    def metadata(self):
        return {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "seed": self.seed,
            "budget": self.budget,
            "completed": self.completed,
        }
