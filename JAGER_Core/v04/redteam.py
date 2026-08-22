from .redteam import RedTeamRunner
from .security import SecurityPolicy


def main():

    runner = RedTeamRunner(
        SecurityPolicy()
    )

    results = runner.run()

    summary = runner.summary(
        results
    )

    print()
    print("=" * 78)
    print("JÄGER v0.4 — RED TEAM SECURITY TEST")
    print("=" * 78)

    for result in results:

        status = (
            "PASS"
            if result["pass"]
            else "FAIL"
        )

        decision = result[
            "decision"
        ]

        print(
            f"{status:4} | "
            f"{result['name']:28} | "
            f"{'ALLOW' if decision['allowed'] else 'DENY ':5} | "
            f"risk={decision['risk']:.2f}"
        )

    print("-" * 78)

    print(
        f"Passed: "
        f"{summary['passed']}/"
        f"{summary['total']}"
    )

    print(
        f"Pass rate: "
        f"{summary['pass_rate'] * 100:.1f}%"
    )

    print("=" * 78)


if __name__ == "__main__":
    main()
