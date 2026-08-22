from .hunter import AdaptiveHunter


def main():
    hunter = AdaptiveHunter(
        seed=42,
        budget=1000,
    )

    print("=" * 60)
    print("JÄGER v0.3 — ADAPTIVE HUNTER")
    print("=" * 60)
    print(f"Run ID: {hunter.run_id}")
    print(f"Seed: {hunter.seed}")
    print(f"Budget: {hunter.budget}")
    print()

    discovery = hunter.run()

    for experiment in hunter.experiments:
        print(
            f"[{experiment.experiment_id}] "
            f"{experiment.status:<9} "
            f"{experiment.strategy:<20} "
            f"reward={experiment.reward:.1f}"
        )

    print()
    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    if discovery:
        print("DISCOVERY FOUND")
        print(f"Discovery ID: {discovery.discovery_id}")
        print(f"Confirmed: {discovery.confirmed}")
        print(
            f"Reproduction attempts: "
            f"{discovery.reproduction_attempts}"
        )
    else:
        print("NO DISCOVERY")

    print(f"Experiments: {len(hunter.experiments)}")
    print(f"Experiences: {len(hunter.memory)}")
    print(f"Discoveries: {len(hunter.discovery_manager.discoveries)}")


if __name__ == "__main__":
    main()
