from .errors import ConfigurationError


def validate_config(config):
    if config.seed < 0:
        raise ConfigurationError(
            "Seed must be non-negative."
        )

    if config.budget <= 0:
        raise ConfigurationError(
            "Budget must be greater than zero."
        )

    if not 0 <= config.exploration_rate <= 1:
        raise ConfigurationError(
            "Exploration rate must be between 0 and 1."
        )

    if config.memory_capacity <= 0:
        raise ConfigurationError(
            "Memory capacity must be greater than zero."
        )

    if config.reproduction_attempts <= 0:
        raise ConfigurationError(
            "Reproduction attempts must be greater than zero."
        )

    return True
