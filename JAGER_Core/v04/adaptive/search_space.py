from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
import random


@dataclass
class ParameterSpec:
    name: str
    kind: str
    minimum: float | int | None = None
    maximum: float | int | None = None
    values: List[Any] = field(
        default_factory=list
    )

    def sample(self, rng: random.Random):

        if self.kind == "float":
            return rng.uniform(
                float(self.minimum),
                float(self.maximum),
            )

        if self.kind == "int":
            return rng.randint(
                int(self.minimum),
                int(self.maximum),
            )

        if self.kind == "choice":

            if not self.values:
                raise ValueError(
                    f"No values defined for "
                    f"{self.name}"
                )

            return rng.choice(
                self.values
            )

        raise ValueError(
            f"Unsupported parameter type: "
            f"{self.kind}"
        )


class SearchSpace:

    def __init__(
        self,
        seed: int = 42,
    ):

        self.rng = random.Random(seed)

        self.parameters: Dict[
            str, ParameterSpec
        ] = {}

    def add_float(
        self,
        name: str,
        minimum: float,
        maximum: float,
    ):

        if minimum > maximum:
            raise ValueError(
                "minimum cannot exceed maximum"
            )

        self.parameters[name] = (
            ParameterSpec(
                name=name,
                kind="float",
                minimum=minimum,
                maximum=maximum,
            )
        )

    def add_int(
        self,
        name: str,
        minimum: int,
        maximum: int,
    ):

        if minimum > maximum:
            raise ValueError(
                "minimum cannot exceed maximum"
            )

        self.parameters[name] = (
            ParameterSpec(
                name=name,
                kind="int",
                minimum=minimum,
                maximum=maximum,
            )
        )

    def add_choice(
        self,
        name: str,
        values: List[Any],
    ):

        if not values:
            raise ValueError(
                "Choice parameter requires "
                "at least one value"
            )

        self.parameters[name] = (
            ParameterSpec(
                name=name,
                kind="choice",
                values=list(values),
            )
        )

    def sample(self):

        return {
            name: spec.sample(self.rng)
            for name, spec
            in self.parameters.items()
        }

    def sample_many(
        self,
        count: int,
    ):

        if count < 0:
            raise ValueError(
                "count cannot be negative"
            )

        return [
            self.sample()
            for _ in range(count)
        ]

    def names(self) -> List[str]:

        return list(
            self.parameters.keys()
        )

    def describe(self):

        return {
            name: {
                "kind": spec.kind,
                "minimum":
                    spec.minimum,
                "maximum":
                    spec.maximum,
                "values":
                    list(spec.values),
            }
            for name, spec
            in self.parameters.items()
        }
