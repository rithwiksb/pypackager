from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback
    import tomli as tomllib  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class DockerConfig:
    base_image: str = "python:3.12-slim"
    entrypoint: Optional[str] = None


@dataclass
class Config:
    targets: List[str] = field(default_factory=lambda: ["wheel", "docker", "binary"])
    docker: DockerConfig = field(default_factory=DockerConfig)


DEFAULT_CONFIG_FILENAMES = ["pypackager.toml", ".pypackager.toml"]


def load_config(project_root: Path, config_path: Optional[Path] = None) -> Config:
    """Load pypackager configuration from TOML or return defaults.

    The file is optional; absence results in default targets.
    """
    if config_path is None:
        for name in DEFAULT_CONFIG_FILENAMES:
            candidate = project_root / name
            if candidate.exists():
                config_path = candidate
                break

    if not config_path or not config_path.exists():
        logger.debug("No config file found; using defaults")
        return Config()

    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    cfg = data.get("pypackager", {})
    targets = cfg.get("targets") or ["wheel", "docker", "binary"]
    
    docker_cfg = cfg.get("docker", {})
    docker_config = DockerConfig(
        base_image=docker_cfg.get("base_image", "python:3.12-slim"),
        entrypoint=docker_cfg.get("entrypoint"),
    )
    
    return Config(targets=list(targets), docker=docker_config)
