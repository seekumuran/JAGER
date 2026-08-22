from .logger import EventLogger


def display_events(
    events,
):

    print()
    print("=" * 110)
    print("JÄGER — SECURITY EVENT VIEW")
    print("=" * 110)

    if not events:

        print("No events recorded.")

        return

    for event in events:

        print(
            f"{event['timestamp']} | "
            f"{event['decision']:5} | "
            f"{event['agent']:8} | "
            f"{event['target']:12} | "
            f"{event['operation']:10} | "
            f"risk={event['risk']:.2f}"
        )

        print(
            f"  trace={event['trace_id']} "
            f"experiment={event['experiment_id']}"
        )

        print(
            f"  reason={event['reason']}"
        )

    print("=" * 110)


def main():

    logger = EventLogger()

    events = logger.read()

    display_events(events)


if __name__ == "__main__":
    main()
