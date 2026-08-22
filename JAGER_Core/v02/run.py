from .experience_hunter import ExperienceHunter


def main():
    hunter = ExperienceHunter(
        seed=42,
        budget=1000,
    )

    print("=" * 55)
    print("JÄGER v0.2 — EXPERIENCE HUNTER")
    print("=" * 55)
    print(f"Run ID: {hunter.run_id}")
    print(f"Seed: {hunter.seed}")
    print(f"Budget: {hunter.budget}")
    print()

    discovery = hunter.run()

    for index, experiment in enumerate(hunter.experiments, start=1):
        print(
            f"[{index:06d}] "
            f"{experiment.status}"
        )

    print()
    print("=" * 55)
    print("RESULT")
    print("=" * 55)

    if discovery:
        print("Status: DISCOVERY FOUND")
    else:
        print("Status: NO DISCOVERY")

    print(f"Experiments executed: {len(hunter.experiments)}")
    print(f"Experiences stored: {len(hunter.memory)}")
    print(f"Discoveries: {len(hunter.discoveries)}")


if __name__ == "__main__":
    main()
