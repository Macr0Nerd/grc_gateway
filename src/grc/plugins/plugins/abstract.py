"""Plugin abstracts.

Attributes:
    ModuleMap (type[dict[str, ModuleType]]): A mapping of a string to a module
"""

import dataclasses
from types import ModuleType
from typing import Any

ModuleMap = dict[str, ModuleType]


@dataclasses.dataclass
class PluginInfo:
    """Plugin information.

    Notes:
        The metadata can be set to anything, but the convention that this
        project follows is that it is a mapping of a plugin name to the metadata
        settings for that plugin. Do not invade the namespaces of other plugins
        -- that's not nice.

    Attributes:
        plugin_name (str): The plugin name.
        plugin_description (Optional[str]): The plugin description.
        plugin_version (Optional[str]): The plugin version.
        plugin_metadata (Optional[dict[str, any]]): The plugin metadata.
    """

    plugin_name: str
    plugin_description: str | None = None
    plugin_version: str | None = None
    plugin_metadata: dict[str, Any] | None = None
