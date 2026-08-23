from typing import Any, Dict, Optional

from .core.api import JagerAPI
from .core.config import JagerConfig
from .core.facade import Jager


def create_api(
    config: Optional[
        JagerConfig
    ] = None,
) -> JagerAPI:

    return JagerAPI(
        Jager(config)
    )


def create_api_from_dict(
    values: Optional[
        Dict[str, Any]
    ] = None,
) -> JagerAPI:

    config = JagerConfig.from_dict(
        values or {}
    )

    return create_api(
        config
    )


__all__ = [
    "JagerAPI",
    "create_api",
    "create_api_from_dict",
]
