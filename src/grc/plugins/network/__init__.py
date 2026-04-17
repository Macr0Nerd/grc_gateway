"""Networking plugin."""

__all__ = []

from grc.dunders import __version__
from grc.plugins.plugins import PluginInfo

plugin_info = PluginInfo(
    plugin_name='network',
    plugin_description='network management plugin',
    plugin_version=__version__,
)
