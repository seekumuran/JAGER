import json

from .hunter import JagerHunter


def main():
    hunter = JagerHunter(
        seed=42,
        budget=1000,
    )

    print("=" * 65)
    print("JÄGER v0.4 — AUTONOMOUS HUNTER")
    print("=" * 65)
    print(f"Run ID: {hunter.run_id}")
    print(f"Seed: {hunter.seed}")
    print(f"Budget: {hunter.budget}")
    print()

    discoveries = hunter.run()

    for experiment in hunter.experiments:
        action = experiment["action"]
        observation = experiment["observation"]
        experience = experiment["experience"]

        print(
            f"{observation.observation_id} | "
            f"{observation.status:<9} | "
            f"reward={experience.reward:>4.1f} | "
            f"novelty={experience.novelty:.1f}"
        )

    print()
    print("=" * 65)
    print("FINAL RESULT")
    print("=" * 65)
    print(f"Experiments: {len(hunter.experiments)}")
    print(f"Memory entries: {len(hunter.memory)}")
    print(f"Failures discovered: {len(discoveries)}")
    print(f"Events generated: {len(hunter.logger.events)}")

    if discoveries:
        print()
        print("FIRST DISCOVERY:")

        first = discoveries[0]

        print(
            json.dumps(
                {
                    "observation_id": first.observation_id,
                    "status": first.observation.status,
                    "inputs": first.action.parameters,
                    "reward": first.reward,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
