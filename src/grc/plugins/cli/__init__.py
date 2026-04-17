"""CLI Application Plugin."""

__all__ = ['cli']

from grc.dunders import __version__
from grc.plugins.cli.application import cli
from grc.plugins.plugins import PluginInfo

plugin_info = PluginInfo(
    plugin_name='cli',
    plugin_description='command line interface plugin',
    plugin_version=__version__,
)
