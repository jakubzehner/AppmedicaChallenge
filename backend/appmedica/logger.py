import json
import logging
import logging.config
import typing as t
from pathlib import Path

from appmedica import config

_logger: t.Optional[logging.Logger] = None


def get_logger(name: str) -> logging.Logger:
    global _logger
    if _logger is None:
        raise ValueError("Logger has not been set up. Call setup_logger first.")

    return _logger.getChild(name)


def setup_logger(level: int = config.LOGGER_LEVEL) -> logging.Logger:
    global _logger
    if _logger is not None:
        return _logger

    path = Path(__file__).parent / "logging.json"
    if not path.exists():
        raise FileNotFoundError(f"Logging configuration file not found: {path}")

    with open(path) as file:
        logging.config.dictConfig(json.loads(file.read()))

    logger = logging.getLogger("appmedica")
    logger.setLevel(level)

    _logger = logger

    return logger
