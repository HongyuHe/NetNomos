from __future__ import annotations

import logging
import sys


LOGGER_NAME = "netn"
DEFAULT_FORMAT = "[%(name)s @ %(asctime)s] %(levelname)-7s | %(message)s"
DEFAULT_DATEFMT = "%H:%M:%S"


class FlushStreamHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord) -> None:
        super().emit(record)
        self.flush()


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    if not logger.handlers:
        handler = FlushStreamHandler(stream=sys.stderr)
        handler.setFormatter(logging.Formatter(DEFAULT_FORMAT, datefmt=DEFAULT_DATEFMT))
        logger.addHandler(handler)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    root = configure_logging()
    if not name:
        return root
    child_name = name if name.startswith(LOGGER_NAME) else f"{LOGGER_NAME}.{name}"
    child = logging.getLogger(child_name)
    child.setLevel(root.level)
    return child
