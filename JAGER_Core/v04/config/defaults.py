from .config import JagerConfig


def default_config():

    return JagerConfig(
        max_iterations=3,
        default_risk_level="low",
        maximum_risk=0.5,
        minimum_candidate_score=0.0,
        novelty_threshold=0.60,
        confidence_threshold=0.70,
        experience_limit=10000,
        execution_timeout_ms=30_000.0,
        allow_unknown_risk=False,
    ).validate()
