"""
Public JAGER entry point.
"""

from typing import Any, Dict, Optional

from .core.config import JagerConfig
from .core.facade import Jager


def create(
    config: Optional[
        JagerConfig
    ] = None,
) -> Jager:

    return Jager(config)


def create_from_dict(
    values: Optional[
        Dict[str, Any]
    ] = None,
) -> Jager:

    config = JagerConfig.from_dict(
        values or {}
    )

    return Jager(config)


__all__ = [
    "Jager",
    "JagerConfig",
    "create",
    "create_from_dict",
]
