from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List

from . import __version__
from .config import load_config
from .core.pipeline import Pipeline
from .logging import setup_logging


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="pypackager", description="Unified build pipeline for Python projects")
    parser.add_argument("command", nargs="?", default="build", choices=["build"], help="Command to run")
    parser.add_argument("project", nargs="?", default=".", help="Path to project root (default: .)")
    parser.add_argument("--version", action="version", version=f"pypackager {__version__}")

    parser.add_argument("--only", dest="only", action="append", choices=["wheel", "docker", "binary"],
                        help="Build only specified target(s); can be used multiple times")
    parser.add_argument("--output", dest="output", default=None, help="Output directory (default: <project>/dist)")
    parser.add_argument("--config", dest="config", default=None, help="Path to pypackager.toml config file")

    vgroup = parser.add_mutually_exclusive_group()
    vgroup.add_argument("-v", dest="verbose", action="count", default=0, help="Increase verbosity (-v, -vv)")
    vgroup.add_argument("-q", dest="quiet", action="store_true", help="Quiet mode")

    parser.add_argument("--log-json", dest="log_json", action="store_true", help="Emit logs as JSON")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)

    # Logging setup
    level = logging.INFO
    if args.quiet:
        level = logging.WARNING
    elif args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose == 1:
        level = logging.INFO

    setup_logging(level=level, json_output=args.log_json)

    project_root = Path(args.project).resolve()
    output_dir = Path(args.output).resolve() if args.output else (project_root / "dist")

    cfg = load_config(project_root, Path(args.config) if args.config else None)
    targets = args.only or cfg.targets

    pipeline = Pipeline(project_root)
    pipeline.run(targets=targets, output_dir=output_dir)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
