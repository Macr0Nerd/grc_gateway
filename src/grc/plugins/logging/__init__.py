"""Logging plugin."""

__all__ = ['configure_logging', 'LOG_CONFIG', 'TemplateStringAdapter']

from grc.dunders import __version__
from grc.plugins.logging.abstract import TemplateStringAdapter
from grc.plugins.logging.utils import LOG_CONFIG, configure_logging
from grc.plugins.plugins import PluginInfo

plugin_info = PluginInfo(
    plugin_name='logging',
    plugin_description='logging and output configuration plugin',
    plugin_version=__version__,
)
