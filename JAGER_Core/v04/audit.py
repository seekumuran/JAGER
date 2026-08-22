from .serialization import dumps


class AuditTrail:
    def __init__(self):
        self.records = []

    def record(self, event):
        self.records.append(event)

    def export(self):
        return dumps(self.records)

    def __len__(self):
        return len(self.records)
