from __future__ import annotations

import abc
from pathlib import Path
from typing import Protocol


class Builder(abc.ABC):
    """Abstract builder interface for artifact generators.

    Each builder implements two steps:
    - configure(project_info): ingest project metadata and prepare internal state
    - build(output_directory): produce artifacts under the given directory
    """

    name: str = "builder"

    @abc.abstractmethod
    def configure(self, project_info: "ProjectInfo") -> None:  # noqa: F821 (forward decl)
        ...

    @abc.abstractmethod
    def build(self, output_directory: Path) -> None:
        ...
