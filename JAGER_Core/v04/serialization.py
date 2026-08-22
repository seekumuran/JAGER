import json
from dataclasses import asdict, is_dataclass


def serialize(value):
    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, list):
        return [serialize(item) for item in value]

    if isinstance(value, dict):
        return {
            key: serialize(item)
            for key, item in value.items()
        }

    return value


def dumps(value, indent=2):
    return json.dumps(
        serialize(value),
        indent=indent,
        sort_keys=True,
    )
