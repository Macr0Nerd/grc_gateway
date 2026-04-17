"""Logging filters module."""

import logging
from typing import Callable


def level_and_below_filter(
    level: int | str,
) -> Callable[[logging.LogRecord], bool]:
    """Logging filter for levels at or below a certain level.

    Args:
        level (Union[int, str]): Logging level

    Returns:
        Callable[[logging.LogRecord], bool]: A callable to determine if the log record is at or below the set level
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())

    def _filter(record: logging.LogRecord) -> bool:
        return record.levelno <= level

    return _filter


filters = {
    'level_below': {
        logging.NOTSET: level_and_below_filter(logging.NOTSET),
        logging.DEBUG: level_and_below_filter(logging.DEBUG),
        logging.INFO: level_and_below_filter(logging.INFO),
        logging.WARNING: level_and_below_filter(logging.WARNING),
        logging.ERROR: level_and_below_filter(logging.ERROR),
        logging.CRITICAL: level_and_below_filter(logging.CRITICAL),
    }
}
"""dict[str, dict[int, Callable]]: Logging filters by type and level"""
