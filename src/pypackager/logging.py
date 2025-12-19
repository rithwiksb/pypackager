from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass


@dataclass
class LogConfig:
    level: int = logging.INFO
    json: bool = False


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(level: int = logging.INFO, json_output: bool = False) -> None:
    handler = logging.StreamHandler(stream=sys.stdout)
    if json_output:
        handler.setFormatter(_JsonFormatter())
    else:
        formatter = logging.Formatter("%(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # Reduce noise from third-party libs if any are used later
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pip").setLevel(logging.WARNING)
