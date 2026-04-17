"""Plugin CLI commands."""

import argparse
import logging

from grc.plugins.logging import TemplateStringAdapter
from grc.plugins.plugins.abstract import PluginInfo
from grc.plugins.plugins.loader import discover_plugins

logger = TemplateStringAdapter(logging.getLogger(__name__))


def add_plugin_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add parser arguments.

    Args:
        subparsers (argparse._SubParsersAction): Plugin arguments subparser
    """
    subparsers.add_parser(
        'list', help='plugins manager', description='plugins manager'
    )


def list(**_) -> int:  # noqa: A001
    """List existing plugins."""
    discovered_plugins = discover_plugins()

    print(f'{"Name":<15} {"Version":<15} {"Description"}')
    print(f'{"=" * 15} {"=" * 15} {"=" * 15}')

    for plugin_path, plugin_module in discovered_plugins.items():
        plugin_info: PluginInfo = plugin_module.plugin_info
        name = plugin_info.plugin_name
        version = plugin_info.plugin_version
        description = plugin_info.plugin_description
        print(
            f'{name:<15} {version if version else "":<15} {description if description else ""}'
        )

    return 0
