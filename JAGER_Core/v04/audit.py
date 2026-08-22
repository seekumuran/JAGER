import hashlib
import json
import time


class AuditTrail:

    def __init__(self):
        self.records = []

    def append(
        self,
        event_type,
        payload,
    ):
        record = {
            "timestamp": time.time(),
            "event_type": event_type,
            "payload": payload,
        }

        canonical = json.dumps(
            record,
            sort_keys=True,
            default=str,
        )

        record["digest"] = hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

        self.records.append(record)

        return record

    def export(self):
        return list(self.records)

    def verify(self):
        for record in self.records:
            digest = record["digest"]

            unsigned = {
                key: value
                for key, value in record.items()
                if key != "digest"
            }

            canonical = json.dumps(
                unsigned,
                sort_keys=True,
                default=str,
            )

            expected = hashlib.sha256(
                canonical.encode("utf-8")
            ).hexdigest()

            if expected != digest:
                return False

        return True
