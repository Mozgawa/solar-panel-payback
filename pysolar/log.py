"""Logger."""

import logging
from typing import Any

_LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"


def get_stream_handler(debug: bool) -> logging.Handler:
    """Get stream handler."""
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    return stream_handler


def get_logger(name: str, debug: bool = False) -> Any:
    """Get logger for module."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        logger.addHandler(get_stream_handler(debug))
    return logger
