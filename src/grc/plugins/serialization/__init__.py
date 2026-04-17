"""Serialization plugin."""

__all__ = ['IsSerialized', 'Serializable', 'serialize']

from grc.dunders import __version__
from grc.plugins.plugins import PluginInfo
from grc.plugins.serialization.abstract import IsSerialized, Serializable
from grc.plugins.serialization.io import serialize

plugin_info = PluginInfo(
    plugin_name='serialization',
    plugin_description='serialization plugin',
    plugin_version=__version__,
)
