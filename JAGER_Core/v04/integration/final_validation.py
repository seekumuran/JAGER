from typing import Any, Dict

from .v04_audit import (
    run_audit,
)

from .v04_imports import (
    run_import_audit,
)

from .test_suite_runner import (
    TestSuiteRunner,
)


def run_final_validation() -> Dict[str, Any]:

    audit = run_audit()

    imports = run_import_audit()

    tests = TestSuiteRunner().run()

    return {
        "audit": audit,
        "imports": imports,
        "tests": {
            "passed":
                tests.passed,
            "return_code":
                tests.return_code,
            "output":
                tests.output,
            "error":
                tests.error,
        },
        "healthy": (
            audit["summary"]["healthy"]
            and imports["summary"]["healthy"]
            and tests.passed
        ),
    }


if __name__ == "__main__":

    report = run_final_validation()

    print(
        "================================"
    )

    print(
        "JÄGER v04 FINAL VALIDATION"
    )

    print(
        "================================"
    )

    print(
        "\nAUDIT"
    )

    print(
        report["audit"]["summary"]
    )

    print(
        "\nIMPORTS"
    )

    print(
        report["imports"]["summary"]
    )

    print(
        "\nTESTS"
    )

    print(
        "PASSED"
        if report["tests"]["passed"]
        else "FAILED"
    )

    print(
        "\nOVERALL"
    )

    print(
        "PASS"
        if report["healthy"]
        else "FAIL"
    )
