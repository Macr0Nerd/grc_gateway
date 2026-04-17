"""Logging utilities.

Attributes:
    LOG_CONFIG (Optional[dict]): logging configuration
"""

import logging
import logging.config

from grc.plugins.logging.filters import filters

LOG_CONFIG: dict | None = None


def configure_logging(
    *,
    output_log_file: str | None = None,
    output_log_level: str | int | None = None,
    quiet: int | None = None,
    verbose: int | None = None,
    suppress_stdout: bool | None = None,
    **_,
) -> None:
    """Configures the logging module.

    Args:
        output_log_file (str): The path to the log file
        output_log_level (str): The log level
        quiet (int): The quiet level
        verbose (int): The verbose level
        suppress_stdout (bool): Suppress stdout
    """
    if output_log_level is None:
        output_log_level = logging.INFO
    elif isinstance(output_log_level, str):
        output_log_level = getattr(logging, output_log_level.upper())

    if quiet and verbose:
        raise ValueError('the quiet and verbose options are mutually exclusive')

    console_log_level = logging.WARNING

    if quiet:
        console_log_level += min(quiet * 10, 20)
    elif verbose:
        console_log_level -= min(verbose * 10, 20)

    global LOG_CONFIG
    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '({asctime}) {name} [{levelname}]: {message}',
                'datefmt': '%H:%M:%S',
                'style': '{',
                'validate': True,
            },
            'file': {
                'format': '{asctime} {name} {levelname}: {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'style': '{',
                'validate': True,
            },
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'level': console_log_level,
                'formatter': 'console',
                'stream': 'ext://sys.stdout',
                'filters': [filters['level_below'][logging.WARNING]],
            },
            'stderr': {
                'class': 'logging.StreamHandler',
                'level': logging.ERROR,
                'formatter': 'console',
                'stream': 'ext://sys.stderr',
            },
        },
        'root': {'level': logging.DEBUG, 'handlers': ['stdout', 'stderr']},
    }

    if suppress_stdout:
        LOG_CONFIG['root']['handlers'].remove('stdout')

    if output_log_file:
        LOG_CONFIG['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': output_log_level,
            'formatter': 'file',
            'filename': output_log_file,
        }

        LOG_CONFIG['root']['handlers'].append('file')

    logging.config.dictConfig(LOG_CONFIG)
