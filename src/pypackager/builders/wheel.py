from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from ..core.builder import Builder
from ..core.environment import isolated_env
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
        project_root = self._project.root

        def _env_python(env_path: Path) -> Path:
            return env_path / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")

        with isolated_env() as env_path:
            py_exe = _env_python(env_path)
            # Install build tooling into the isolated environment
            subprocess.check_call([str(py_exe), "-m", "pip", "install", "build>=1.1.1"], cwd=project_root)  # noqa: S603,S607
            # Produce both wheel and sdist to support downstream packaging steps
            subprocess.check_call([str(py_exe), "-m", "build", "--wheel", "--sdist", "--outdir", str(output_directory)], cwd=project_root)  # noqa: S603,S607

        logger.info("Wheel builder produced artifacts in %s", output_directory)
