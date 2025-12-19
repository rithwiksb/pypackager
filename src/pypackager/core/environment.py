from __future__ import annotations

import logging
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
import venv

logger = logging.getLogger(__name__)


class _EnvBuilder(venv.EnvBuilder):
    def post_setup(self, context) -> None:  # type: ignore[override]
        # ensure pip is available
        try:
            subprocess.check_call([context.env_exe, "-m", "pip", "--version"])  # noqa: S603,S607
        except Exception:
            logger.warning("pip not available in venv at %s", context.env_dir)


@contextmanager
def isolated_env() -> Path:
    """Create an ephemeral isolated virtual environment and yield its path.

    The environment is deleted on exit.
    """
    tmpdir = Path(tempfile.mkdtemp(prefix="pypackager-venv-"))
    env_path = tmpdir / "venv"
    builder = _EnvBuilder(with_pip=True, clear=False, symlinks=True)
    builder.create(str(env_path))
    logger.info("Created isolated environment at %s", env_path)
    try:
        yield env_path
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        logger.info("Removed isolated environment at %s", env_path)
