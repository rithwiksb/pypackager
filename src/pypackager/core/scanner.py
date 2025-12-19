from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback
    import tomli as tomllib  # type: ignore

from .project import ProjectInfo

logger = logging.getLogger(__name__)


class ProjectScanner:
    """Scan a Python project and derive metadata from PEP 621 pyproject.toml.

    MVP: require pyproject.toml with PEP 621 fields `project.name`, `project.version`.
    Legacy setup.py support will be added later.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.pyproject_path = project_root / "pyproject.toml"

    def scan(self) -> ProjectInfo:
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}")

        data = tomllib.loads(self.pyproject_path.read_text(encoding="utf-8"))
        project = data.get("project") or {}

        name = project.get("name")
        version = project.get("version")
        if not name or not version:
            raise ValueError("project.name and project.version are required in pyproject.toml")

        requires_python: Optional[str] = project.get("requires-python")
        deps: List[str] = list(project.get("dependencies") or [])

        info = ProjectInfo(
            name=name,
            version=str(version),
            root=self.project_root,
            python_requires=requires_python,
            dependencies=deps,
        )
        logger.debug("Scanned project: %s", info)
        return info
