from typing import List, Dict, Any

from .scenarios import get_scenarios


class RedTeamRunner:

    def __init__(self, policy):

        self.policy = policy

    def run(self):

        results = []

        for scenario in get_scenarios():

            action = scenario.attack()

            decision = self.policy.evaluate(
                action
            )

            actual_allowed = (
                decision.allowed
            )

            passed = (
                actual_allowed
                == scenario.expected_allowed
            )

            results.append(
                {
                    "name": scenario.name,
                    "description":
                        scenario.description,
                    "expected_allowed":
                        scenario.expected_allowed,
                    "actual_allowed":
                        actual_allowed,
                    "decision":
                        decision.to_dict(),
                    "pass": passed,
                }
            )

        return results

    @staticmethod
    def summary(
        results: List[Dict[str, Any]]
    ):

        total = len(results)

        passed = sum(
            1
            for result in results
            if result["pass"]
        )

        failed = total - passed

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (
                passed / total
                if total
                else 0.0
            ),
        }
