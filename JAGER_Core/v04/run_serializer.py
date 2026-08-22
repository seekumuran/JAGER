from dataclasses import asdict, is_dataclass


def serialize(value):

    if is_dataclass(value):
        return serialize(
            asdict(value)
        )

    if isinstance(value, dict):
        return {
            str(key): serialize(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            serialize(item)
            for item in value
        ]

    if hasattr(value, "to_dict"):
        return serialize(
            value.to_dict()
        )

    return value


def serialize_experiment(
    experiment
):
    return serialize(
        experiment
    )


def serialize_experiments(
    experiments
):
    return [
        serialize_experiment(
            experiment
        )
        for experiment in experiments
    ]
