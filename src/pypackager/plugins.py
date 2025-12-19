from __future__ import annotations

import logging
from typing import Dict, Type

try:
    from importlib import metadata as importlib_metadata
except Exception:  # pragma: no cover
    import importlib_metadata  # type: ignore

logger = logging.getLogger(__name__)


def discover_builders() -> Dict[str, Type]:
    """Discover builder classes via entry points group 'pypackager.builders'.

    When running from source (uninstalled), fall back to built-in builders.
    """
    try:
        eps = importlib_metadata.entry_points()
        if hasattr(eps, "select"):
            entries = eps.select(group="pypackager.builders")  # type: ignore[attr-defined]
        else:  # Python 3.9 fallback shape
            entries = eps.get("pypackager.builders", [])  # type: ignore[index]
    except Exception as e:  # pragma: no cover
        logger.warning("Failed to discover entry points: %s", e)
        entries = []

    result: Dict[str, Type] = {}
    for ep in entries:
        try:
            cls = ep.load()
            result[ep.name] = cls
        except Exception as e:  # pragma: no cover
            logger.warning("Failed to load builder '%s': %s", getattr(ep, "name", "?"), e)

    # Fallback: import built-in builders directly when entry points are unavailable
    if not result:
        try:
            from .builders.wheel import WheelBuilder  # type: ignore
            from .builders.docker import DockerBuilder  # type: ignore
            from .builders.binary import BinaryBuilder  # type: ignore

            result = {
                "wheel": WheelBuilder,
                "docker": DockerBuilder,
                "binary": BinaryBuilder,
            }
            logger.debug("Using built-in builders fallback discovery")
        except Exception as e:  # pragma: no cover
            logger.warning("Fallback builder import failed: %s", e)

    return result
