from ..api.jager import Jager

from ..config.defaults import (
    default_config,
)

from ..executor.mock_target_adapter import (
    MockTargetAdapter,
)

from ..executor.target_registry import (
    TargetRegistry,
)

from .final_audit import (
    FinalAudit,
)


def build_audit():

    registry = TargetRegistry()

    registry.register(
        MockTargetAdapter("mock")
    )

    jager = Jager(
        registry=registry,
        config=default_config(),
    )

    audit = FinalAudit()

    audit.register(
        "configuration",
        lambda:
            jager.config is not None,
    )

    audit.register(
        "target_registry",
        lambda:
            "mock"
            in jager.targets(),
    )

    audit.register(
        "runtime",
        lambda:
            jager.runtime is not None,
    )

    audit.register(
        "runtime_state",
        lambda:
            jager.status() is not None,
    )

    audit.register(
        "public_api",
        lambda:
            callable(jager.run),
    )

    audit.register(
        "reset",
        lambda:
            callable(jager.reset),
    )

    return audit


def run_audit():

    audit = build_audit()

    results = audit.run()

    return {
        "results": [
            {
                "name":
                    result.name,
                "passed":
                    result.passed,
                "message":
                    result.message,
            }
            for result in results
        ],
        "summary":
            audit.summary(),
    }


if __name__ == "__main__":

    report = run_audit()

    print(
        "JÄGER v04 FINAL AUDIT"
    )

    for result in report[
        "results"
    ]:

        marker = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"[{marker}] "
            f"{result['name']}: "
            f"{result['message']}"
        )

    print(
        "\nSUMMARY"
    )

    print(
        report["summary"]
    )
