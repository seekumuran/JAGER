from typing import Dict, Any


class AnomalyReport:

    def build(
        self,
        target: str,
        experiment_id: str,
        anomalies: Dict[str, Any],
    ):

        detected = [
            anomaly.to_dict()
            for anomaly in anomalies.values()
            if anomaly.anomalous
        ]

        return {
            "target": target,
            "experiment_id":
                experiment_id,
            "anomaly_count":
                len(detected),
            "anomalous":
                bool(detected),
            "anomalies":
                detected,
        }

    def severity(
        self,
        anomalies: Dict[str, Any],
    ):

        if not anomalies:
            return "NONE"

        maximum = max(
            anomaly.score
            for anomaly
            in anomalies.values()
        )

        if maximum >= 5.0:
            return "CRITICAL"

        if maximum >= 3.0:
            return "HIGH"

        if maximum >= 2.0:
            return "MEDIUM"

        if maximum > 0:
            return "LOW"

        return "NONE"
``
