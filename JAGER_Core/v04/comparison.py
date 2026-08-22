from .statistics import rate


def compare_runs(jager_results, baseline_results):
    jager_failures = sum(
        result["observation"].status == "FAILED"
        for result in jager_results
    )

    baseline_failures = sum(
        result["result"]["status"] == "FAILED"
        for result in baseline_results
    )

    jager_total = len(jager_results)
    baseline_total = len(baseline_results)

    return {
        "jager": {
            "experiments": jager_total,
            "failures": jager_failures,
            "failure_rate": rate(
                jager_failures,
                jager_total,
            ),
        },
        "baseline": {
            "experiments": baseline_total,
            "failures": baseline_failures,
            "failure_rate": rate(
                baseline_failures,
                baseline_total,
            ),
        },
    }
