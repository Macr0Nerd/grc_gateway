"""Plugins loaders."""

import importlib
import logging
import pkgutil
from types import ModuleType
from typing import Any, Iterator

import grc.plugins
from grc.plugins.logging import TemplateStringAdapter
from grc.plugins.plugins.abstract import ModuleMap
from grc.plugins.plugins.filters import MetadataFilter

logger = TemplateStringAdapter(logging.getLogger(__name__))


def discover_plugins() -> ModuleMap:
    """Discover all plugins and return a dictionary mapping plugin names to modules.

    Returns:
        ModuleMap: a dictionary mapping plugin names to modules
    """

    def iter_namespace(ns_pkg: ModuleType) -> Iterator[pkgutil.ModuleInfo]:
        """Iterate a namespace package and an iterator of submodule information.

        Args:
            ns_pkg (ModuleType): a namespace package

        Returns:
            Iterator[pkgutil.ModuleInfo]: an iterator of submodule information
        """
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + '.')

    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(grc.plugins)
    }

    valid_plugins = {}

    for plugin_name, plugin_module in discovered_plugins.items():
        if not hasattr(plugin_module, 'plugin_info'):
            logger.warning(
                t'Plugin {plugin_name} has no plugin_info attribute, skipping'
            )
            continue

        valid_plugins[plugin_name] = plugin_module

    return valid_plugins


def filter_plugins_metadata(
    filters: dict[str, Any | None], plugins: ModuleMap | None = None
) -> ModuleMap:
    """Filter plugins metadata based on filters.

    Notes:
        * If plugins are not provided this calls discover_plugins().

    Args:
        filters (dict[str, Optional[Any]]): metadata filters
        plugins (Optional[ModuleMap]): the plugins list

    Returns:
        Optional[ModuleMap]: plugins matching the filters

    References:
        * grc.plugins.plugins.filters.MetadataFilter
    """
    if not plugins:
        plugins = discover_plugins()

    filtered_plugins: ModuleMap = {}

    metadata_filter = MetadataFilter(filters)

    for plugin_name, plugin_module in plugins.items():
        if metadata_filter(plugin_module.plugin_info):
            filtered_plugins[plugin_name] = plugin_module

    return filtered_plugins
