"""GRC Gateway Exports."""

__all__ = ['app', 'cli']

from grc.plugins.cli import cli
from grc.plugins.webserver import app
