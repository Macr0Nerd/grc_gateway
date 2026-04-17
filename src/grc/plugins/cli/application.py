"""CLI application module.

This module defines the CLI application. The command line interface is one of two supported entrypoints for the
gateway application. This handles loading all plugins and their arguments from the command line and setting up the
application.
"""

import argparse
import logging

from grc.dunders import __author__, __version__
from grc.plugins.cli.abstract import PluginMetadata
from grc.plugins.logging import TemplateStringAdapter, configure_logging
from grc.plugins.plugins import ModuleMap, PluginInfo
from grc.plugins.plugins.loader import filter_plugins_metadata

logger = TemplateStringAdapter(logging.getLogger(__name__))


def add_miscellaneous_arguments(parser: argparse.ArgumentParser) -> None:
    """Add miscellaneous arguments.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add arguments to
    """
    miscellaneous_group = parser.add_argument_group('miscellaneous')

    miscellaneous_group.add_argument('-h', '--help', action='help')
    miscellaneous_group.add_argument(
        '-V', '--version', action='version', version=__version__
    )


def add_logging_arguments(parser: argparse.ArgumentParser) -> None:
    """Add logging arguments.

    Args:
        parser (argparse.ArgumentParser): Argument parser to add arguments to
    """
    console_logging_group = parser.add_argument_group('console logging options')

    console_logging_group_me = (
        console_logging_group.add_mutually_exclusive_group()
    )
    console_logging_group_me.add_argument(
        '-v', '--verbose', help='increase console log level', action='count'
    )
    console_logging_group_me.add_argument(
        '-q', '--quiet', help='decrease console log level', action='count'
    )

    console_logging_group.add_argument('--suppress-stdout', action='store_true')

    file_logging_group = parser.add_argument_group('file logging options')
    file_logging_group.add_argument(
        '--output-log-file', help='main log file to use', metavar='FILE'
    )
    file_logging_group.add_argument(
        '--output-log-level',
        help='file logging level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    )


def cli() -> int:
    """Command line interface for GRC Gateway.

    Returns:
        int: Exit code
    """
    root_parser = argparse.ArgumentParser(
        description='GRC Gateway Project',
        epilog=f'With love from {__author__} <3',
        add_help=False,
    )

    # Configure logging first so we can use it when discovering plugins if necessary
    add_logging_arguments(root_parser)
    logging_args, cli_args = root_parser.parse_known_args()
    configure_logging(**vars(logging_args))

    commands_plugins: ModuleMap = filter_plugins_metadata({'cli': None})
    command_modules: ModuleMap = {}

    subparsers = root_parser.add_subparsers(
        help='plugin help', dest='plugin', metavar='PLUGIN', required=True
    )
    for plugin_path, plugin_module in commands_plugins.copy().items():
        plugin_info: PluginInfo = plugin_module.plugin_info
        plugin_metadata: dict | PluginMetadata = plugin_info.plugin_metadata[
            'cli'
        ]

        if isinstance(plugin_metadata, dict):
            plugin_metadata = PluginMetadata(**plugin_metadata)

        plugin_parser_kwargs = {
            'name': plugin_info.plugin_name,
            'help': f'{plugin_info.plugin_name} help',
        }
        if plugin_info.plugin_description:
            plugin_parser_kwargs['description'] = plugin_info.plugin_description

        plugin_parser = subparsers.add_parser(**plugin_parser_kwargs)
        plugin_subparsers = plugin_parser.add_subparsers(
            help='command help',
            dest='command',
            metavar='COMMAND',
            required=True,
        )

        plugin_metadata.arguments_callable(plugin_subparsers)

        if plugin_subparsers.choices:
            for _, choice in plugin_subparsers.choices.items():
                add_logging_arguments(choice)

            command_modules[plugin_info.plugin_name] = (
                plugin_metadata.command_module
            )

        add_logging_arguments(plugin_parser)

    add_miscellaneous_arguments(root_parser)

    args = vars(root_parser.parse_args())

    try:
        return getattr(command_modules[args['plugin']], args['command'])(**args)
    except AttributeError:
        logger.error(
            t'Plugin "{args["plugin"]}" has no command "{args["command"]}"'
        )
        return 2
    except ImportError:
        logger.error(
            t'Plugin "{args["plugin"]}" does not properly implement the plugin specification; exiting'
        )
        return 1
    except Exception as e:
        logger.error(t'{e}')
        return 3
