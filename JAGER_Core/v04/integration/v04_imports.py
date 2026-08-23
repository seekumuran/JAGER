from .import_audit import (
    ImportAudit,
)


CORE_MODULES = [
    "JAGER_Core.v04.api",
    "JAGER_Core.v04.config",
    "JAGER_Core.v04.executor",
    "JAGER_Core.v04.persistence",
    "JAGER_Core.v04.recovery",
    "JAGER_Core.v04.state",
    "JAGER_Core.v04.orchestrator",
    "JAGER_Core.v04.integration",
]


def run_import_audit():

    audit = ImportAudit(
        CORE_MODULES
    )

    results = audit.run()

    return {
        "results": [
            {
                "module":
                    result.module,
                "imported":
                    result.imported,
                "error":
                    result.error,
            }
            for result in results
        ],
        "summary":
            audit.summary(),
    }


if __name__ == "__main__":

    report = run_import_audit()

    print(
        "JÄGER v04 IMPORT AUDIT"
    )

    for result in report[
        "results"
    ]:

        marker = (
            "PASS"
            if result["imported"]
            else "FAIL"
        )

        print(
            f"[{marker}] "
            f"{result['module']}"
        )

        if result["error"]:

            print(
                f"       {result['error']}"
            )

    print(
        "\nSUMMARY"
    )

    print(
        report["summary"]
    )
