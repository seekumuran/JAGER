from typing import Optional

from .experience_repository import (
    ExperienceRepository,
)

from .memory_experience_repository import (
    MemoryExperienceRepository,
)

from .json_experience_repository import (
    JsonExperienceRepository,
)


def create_experience_repository(
    backend: str = "memory",
    path: Optional[str] = None,
    maximum_size: int = 10000,
) -> ExperienceRepository:

    if backend == "memory":

        return MemoryExperienceRepository(
            maximum_size=maximum_size
        )

    if backend == "json":

        if not path:
            raise ValueError(
                "path is required for "
                "JSON experience storage"
            )

        return JsonExperienceRepository(
            path=path,
            maximum_size=maximum_size,
        )

    raise ValueError(
        f"Unsupported repository backend: "
        f"{backend}"
    )
