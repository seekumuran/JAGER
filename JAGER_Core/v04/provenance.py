import hashlib
import json


def fingerprint(value):
    encoded = json.dumps(
        value,
        sort_keys=True,
        default=str,
    ).encode("utf-8")

    return hashlib.sha256(encoded).hexdigest()


class Provenance:
    def __init__(self):
        self.records = []

    def record(
        self,
        action,
        observation,
        decision,
    ):
        self.records.append(
            {
                "action": fingerprint(action),
                "observation": fingerprint(observation),
                "decision": fingerprint(decision),
            }
        )

    def export(self):
        return list(self.records)
