from .ai_sandbox import AISandbox


def main():

    sandbox = AISandbox(seed=42)

    requests = [
        (
            "summarize",
            {
                "text": "Synthetic input"
            },
        ),
        (
            "read_context",
            {
                "context": "Synthetic context"
            },
        ),
        (
            "execute_shell",
            {
                "command": "id"
            },
        ),
        (
            "read_context",
            {
                "credential_access": True
            },
        ),
        (
            "generate",
            {
                "network_exfiltration": True
            },
        ),
    ]

    print()
    print("=" * 60)
    print("JÄGER v0.4 — AI SANDBOX")
    print("=" * 60)

    for operation, payload in requests:

        result = sandbox.execute(
            operation,
            payload,
        )

        print(
            f"{operation:20} "
            f"{result['decision']:6} "
            f"{result['reason']}"
        )

    print()

    print(
        sandbox.observe()
    )

    print("=" * 60)


if __name__ == "__main__":
    main()
