from __future__ import annotations

import logging
from pathlib import Path

from ..core.builder import Builder
from ..core.project import ProjectInfo

logger = logging.getLogger(__name__)


class WheelBuilder(Builder):
    name = "wheel"

    def __init__(self) -> None:
        self._project: ProjectInfo | None = None

    def configure(self, project_info: ProjectInfo) -> None:
        self._project = project_info

    def build(self, output_directory: Path) -> None:
        if not self._project:
            raise RuntimeError("WheelBuilder not configured")
        output_directory.mkdir(parents=True, exist_ok=True)
        marker = output_directory / f"{self._project.name}-{self._project.version}-WHEEL.txt"
        marker.write_text(
            "Placeholder artifact. Wheel build integration will follow.\n",
            encoding="utf-8",
        )
        logger.info("Wheel builder produced placeholder artifact at %s", marker)
