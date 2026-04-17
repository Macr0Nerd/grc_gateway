"""Plugins plugin."""

__all__ = ['PluginInfo', 'ModuleMap']

import grc.plugins.plugins.command as command
from grc.dunders import __version__
from grc.plugins.plugins.abstract import ModuleMap, PluginInfo

plugin_info = PluginInfo(
    plugin_name='plugins',
    plugin_description='plugin management plugin',
    plugin_version=__version__,
    plugin_metadata={
        'cli': {
            'arguments_callable': command.add_plugin_parser,
            'command_module': command,
        }
    },
)
