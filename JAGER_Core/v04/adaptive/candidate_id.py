import hashlib
import json


class CandidateID:

    @staticmethod
    def generate(
        target: str,
        parameters,
    ) -> str:

        payload = {
            "target": target,
            "parameters": parameters,
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
            default=str,
        ).encode("utf-8")

        digest = hashlib.sha256(
            encoded
        ).hexdigest()

        return f"cand-{digest[:16]}"
