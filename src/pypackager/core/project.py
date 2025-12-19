from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ProjectInfo:
    name: str
    version: str
    root: Path
    python_requires: Optional[str]
    dependencies: List[str]
