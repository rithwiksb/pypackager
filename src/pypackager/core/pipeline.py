from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, List, Mapping

from .project import ProjectInfo
from .scanner import ProjectScanner
from .resolver import DependencyResolver
from .environment import isolated_env
from ..plugins import discover_builders
from ..config import Config

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, project_root: Path, config: Config | None = None) -> None:
        self.project_root = project_root
        self.config = config

    def run(self, targets: Iterable[str], output_dir: Path) -> None:
        scanner = ProjectScanner(self.project_root)
        project = scanner.scan()

        resolver = DependencyResolver(self.project_root)
        resolver.write_lockfile(project.name, project.version, project.dependencies)

        builders = discover_builders()
        selected = self._select_builders(builders, set(targets))
        if not selected:
            raise ValueError("No builders selected or discovered")

        output_dir.mkdir(parents=True, exist_ok=True)

        for name, builder_cls in selected.items():
            # Pass config to docker builder
            if name == "docker" and self.config:
                builder = builder_cls(
                    base_image=self.config.docker.base_image,
                    entrypoint=self.config.docker.entrypoint
                )
            else:
                builder = builder_cls()
            
            logger.info("Configuring builder: %s", name)
            builder.configure(project)
            with isolated_env() as _env:
                # Future: install deps and tools in env
                artifact_dir = output_dir / name
                artifact_dir.mkdir(parents=True, exist_ok=True)
                logger.info("Running builder: %s", name)
                builder.build(artifact_dir)

    @staticmethod
    def _select_builders(
        available: Mapping[str, type], requested: set[str]
    ) -> Mapping[str, type]:
        if not requested:
            return available
        return {k: v for k, v in available.items() if k in requested}
