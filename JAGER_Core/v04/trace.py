import uuid
import time


class Trace:
    def __init__(self):
        self.trace_id = f"trace-{uuid.uuid4().hex[:12]}"
        self.created_at = time.time()
        self.events = []

    def add(self, event):
        self.events.append(event)

    def summary(self):
        return {
            "trace_id": self.trace_id,
            "created_at": self.created_at,
            "event_count": len(self.events),
        }
