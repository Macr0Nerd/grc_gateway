"""Webserver plugin."""

__all__ = ['app']

import grc.plugins.webserver.command as command
from grc.dunders import __version__
from grc.plugins.plugins import PluginInfo
from grc.plugins.webserver.abstract import App

app = App
"""grc.plugins.webserver.abstract.App: ASGI webserver application"""

plugin_info = PluginInfo(
    plugin_name='webserver',
    plugin_description='webserver management plugin',
    plugin_version=__version__,
    plugin_metadata={
        'cli': {
            'arguments_callable': command.add_plugin_parser,
            'command_module': command,
        }
    },
)
