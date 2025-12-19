from __future__ import annotations

import logging
from pathlib import Path

from ..core.builder import Builder
from ..core.project import ProjectInfo

logger = logging.getLogger(__name__)


class DockerBuilder(Builder):
    name = "docker"

    def __init__(self) -> None:
        self._project: ProjectInfo | None = None

    def configure(self, project_info: ProjectInfo) -> None:
        self._project = project_info

    def build(self, output_directory: Path) -> None:
        if not self._project:
            raise RuntimeError("DockerBuilder not configured")
        output_directory.mkdir(parents=True, exist_ok=True)
        dockerfile = output_directory / "Dockerfile"
        base = "python:3.12-slim"  # default; real build should match project's range
        dockerfile.write_text(
            f"""
FROM {base} AS runtime
WORKDIR /app
COPY . /app
CMD [\"python\", \"-c\", \"print('Replace with app entrypoint')\"]
""".lstrip(),
            encoding="utf-8",
        )
        logger.info("Docker builder wrote Dockerfile at %s", dockerfile)
