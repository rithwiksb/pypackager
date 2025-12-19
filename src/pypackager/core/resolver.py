from __future__ import annotations

import datetime as _dt
import logging
from pathlib import Path
from typing import Iterable, List

logger = logging.getLogger(__name__)


class DependencyResolver:
    """Dependency resolver stub for MVP scaffolding.

    MVP: produce a TOML lockfile with declared dependencies.
    Note: future implementation will resolve dependencies using pip in isolated environments.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def write_lockfile(self, name: str, version: str, dependencies: Iterable[str]) -> Path:
        lock_path = self.project_root / "pypackager.lock"
        deps = list(dependencies)
        created = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        # lightweight TOML emit to avoid a writer dependency
        body = [
            f"# pypackager lockfile (MVP stub)\n",
            f"# created: {created}\n",
            "[project]\n",
            f"name = \"{name}\"\n",
            f"version = \"{version}\"\n",
            "\n[dependencies]\n",
        ]
        for i, dep in enumerate(deps):
            body.append(f"dep{i} = \"{dep}\"\n")
        lock_path.write_text("".join(body), encoding="utf-8")
        logger.info("Wrote lockfile: %s", lock_path)
        return lock_path
